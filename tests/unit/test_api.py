import time

import pytest
from fastapi.testclient import TestClient

from actwise.agent.classifier import ClassificationError, ClassifyOutcome
from actwise.agent.schemas import DISCLAIMER, Classification
from actwise.api.main import MAX_UPLOAD, REQUEST_BUDGET, create_app
from actwise.generation.rag import AskResult, sources_of
from actwise.llm.base import LLMResponse
from actwise.llm.wrappers import LLMUnavailable
from actwise.retrieval.passages import Passage, to_hit

HITS = [to_hit(Passage("AIA-Art5-1#2", "en", "AI Act Article 5(1)\nThe following..."), 0.8)]
QUESTION = {"question": "Is social scoring banned?", "lang": "en"}
DESCRIPTION = "A city scores its residents' trustworthiness from their behaviour."
RESULT = Classification(
    tier="prohibited", reasons=["Social scoring."], citations=["AIA-Art5-1"], confidence=0.9
)


class Pipelines:
    """Fake pipelines: canned results (or `error`), and the deadline of every call."""

    def __init__(self, error=None):
        """Answer every call, or raise `error`."""
        self.error, self.deadlines, self.descriptions = error, [], []

    def ask(self, question, lang, deadline):
        """A cited answer from HITS."""
        self.deadlines.append(deadline)
        if self.error:
            raise self.error
        reply = LLMResponse("Banned [AIA-Art5-1].", [], 10, 5, "gemini-test")
        return AskResult(reply.text, "", ["AIA-Art5-1"], [], sources_of(HITS, lang), reply)

    def classify(self, description, deadline):
        """The prohibited RESULT."""
        self.deadlines.append(deadline)
        self.descriptions.append(description)
        if self.error:
            raise self.error
        return ClassifyOutcome(RESULT, steps=2, lookups=1)

    def search(self, query, top_k):
        """HITS, best first."""
        return HITS[:top_k]


def client(pipelines=None, **options):
    """A test client for the API around `pipelines`."""
    p = pipelines or Pipelines()
    return TestClient(create_app(p.ask, p.classify, p.search, **options))


def test_api_contract():
    """JSON on success; 401 for a bad key, 422 for bad input, 415 for a .exe, 429 after the cap."""
    api = client(api_key="secret", daily_cap=2)
    key = {"X-API-Key": "secret"}

    assert api.get("/health").json()["status"] == "ok"  # the one route without a key
    assert api.get("/search", params={"q": "ban"}).status_code == 401
    assert api.post("/ask", json=QUESTION, headers={"X-API-Key": "wrong"}).status_code == 401
    assert api.post("/ask", json=QUESTION | {"lang": "de"}, headers=key).status_code == 422
    assert api.post("/classify", json={"description": "Too short."}, headers=key).status_code == 422
    exe = api.post("/upload", files={"file": ("setup.exe", b"MZ")}, headers=key)
    assert exe.status_code == 415
    [hit] = api.get("/search", params={"q": "ban"}, headers=key).json()
    answer = api.post("/ask", json=QUESTION, headers=key).json()
    tier = api.post("/classify", json={"description": DESCRIPTION}, headers=key).json()
    over = api.post("/classify", json={"description": DESCRIPTION}, headers=key)

    assert (hit["id"], hit["label"], hit["score"]) == ("AIA-Art5-1", "AI Act, Art. 5(1)", 0.8)
    assert answer["citations"] == ["AIA-Art5-1"] and answer["model"] == "gemini-test"
    assert tier["tier"] == "prohibited" and tier["citations"] == ["AIA-Art5-1"]
    assert answer["disclaimer"] == tier["disclaimer"] == DISCLAIMER
    assert over.status_code == 429  # the cap counts only the requests that reach a model


@pytest.mark.parametrize(
    ("name", "data", "status"),
    [
        ("system.txt", DESCRIPTION.encode(), 200),
        ("big.txt", b"x" * (MAX_UPLOAD + 1), 413),
        ("empty.txt", b"   ", 422),
        ("broken.pdf", b"not a pdf", 422),
    ],
    ids=["text", "too-big", "empty", "broken"],
)
def test_upload(name, data, status):
    """A readable file under 2 MB is classified from its text; anything else is refused."""
    pipelines = Pipelines()

    response = client(pipelines).post("/upload", files={"file": (name, data)})

    assert response.status_code == status
    assert pipelines.descriptions == ([DESCRIPTION] if status == 200 else [])


@pytest.mark.parametrize("error", [LLMUnavailable("no LLM"), ClassificationError("8 steps")])
def test_model_failures_return_503(error):
    """No model answered in time, or no valid classification: 503 with the reason."""
    response = client(Pipelines(error)).post("/classify", json={"description": DESCRIPTION})

    assert (response.status_code, response.json()["detail"]) == (503, str(error))


def test_one_deadline_per_request():
    """Each request gets one deadline, REQUEST_BUDGET from its start, for all its calls (R5)."""
    pipelines = Pipelines()
    api = client(pipelines)

    start = time.monotonic()
    api.post("/ask", json=QUESTION)
    api.post("/classify", json={"description": DESCRIPTION})

    assert all(
        start + REQUEST_BUDGET <= d <= time.monotonic() + REQUEST_BUDGET
        for d in pipelines.deadlines
    )
    assert len(pipelines.deadlines) == 2


def test_register_failure_is_ignored():
    """If the register raises, /classify still returns the classification."""

    class BrokenRegister:
        def log(self, description, result):
            """Fail like a Google Sheets outage."""
            raise ConnectionError("Sheets is down")

    response = client(register=BrokenRegister()).post(
        "/classify", json={"description": DESCRIPTION}
    )

    assert response.status_code == 200 and response.json()["tier"] == "prohibited"
