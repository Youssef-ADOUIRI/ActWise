import time

import pytest
from fastapi.testclient import TestClient

from actwise.agent.classifier import ClassificationError, ClassifyOutcome
from actwise.agent.schemas import DISCLAIMER, Classification
from actwise.api.main import MAX_TOP_K, MAX_UPLOAD, REQUEST_BUDGET, create_app
from actwise.generation.rag import RagPipeline
from actwise.llm.base import LLMResponse
from actwise.llm.wrappers import LLMUnavailable
from actwise.retrieval.passages import Passage, to_hit
from tests.unit.toys import ScriptedLLM

HITS = [to_hit(Passage("AIA-Art5-1#2", "en", "AI Act Article 5(1)\nThe following..."), 0.8)]
REPLY = LLMResponse("Banned [AIA-Art5-1].", [], 10, 5, "gemini-test")
QUESTION = {"question": "Is social scoring banned?", "lang": "en"}
DESCRIPTION = "A city scores its residents' trustworthiness from their behaviour."
RESULT = Classification(
    tier="prohibited", reasons=["Social scoring."], citations=["AIA-Art5-1"], confidence=0.9
)


def search(query, top_k):
    """Fake retriever: HITS, best first."""
    return HITS[:top_k]


class FakeClassifier:
    """Returns RESULT, or raises `error`; records each (description, deadline)."""

    def __init__(self, error=None):
        """Classify every description, or raise `error`."""
        self.error, self.calls = error, []

    def __call__(self, description, deadline):
        """The prohibited RESULT."""
        self.calls.append((description, deadline))
        if self.error:
            raise self.error
        return ClassifyOutcome(RESULT, steps=2, lookups=1)


def client(classifier=None, llm=None, **options):
    """The API around the real RagPipeline on a scripted model, and a fake classifier."""
    rag = RagPipeline(llm or ScriptedLLM(REPLY), search, "Answer from the sources.")
    return TestClient(create_app(rag.ask, classifier or FakeClassifier(), search, **options))


def test_api_contract():
    """JSON on success; 401 for a bad key, 422 for bad input, 415 for a .exe, 429 after the cap."""
    api = client(api_key="secret", daily_cap=2)
    key = {"X-API-Key": "secret"}

    assert api.get("/health").json()["status"] == "ok"  # the one route without a key
    assert api.get("/search", params={"q": "ban"}).status_code == 401
    assert api.post("/ask", json=QUESTION, headers={"X-API-Key": "wrong"}).status_code == 401
    invalid = [
        api.post("/ask", json=QUESTION | {"lang": "de"}, headers=key),
        api.post("/ask", json=QUESTION | {"question": "      "}, headers=key),
        api.post("/classify", json={"description": "Too short."}, headers=key),
        api.get("/search", params={"q": "ban", "top_k": MAX_TOP_K + 1}, headers=key),
    ]
    exe = api.post("/upload", files={"file": ("setup.exe", b"MZ")}, headers=key)
    [hit] = api.get("/search", params={"q": "ban"}, headers=key).json()
    answer = api.post("/ask", json=QUESTION, headers=key).json()
    tier = api.post("/classify", json={"description": DESCRIPTION}, headers=key).json()
    over = api.post("/classify", json={"description": DESCRIPTION}, headers=key)

    assert [response.status_code for response in invalid] == [422] * 4
    assert exe.status_code == 415
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
    classifier = FakeClassifier()

    response = client(classifier).post("/upload", files={"file": (name, data)})

    assert response.status_code == status
    assert [description for description, _ in classifier.calls] == (
        [DESCRIPTION] if status == 200 else []
    )


@pytest.mark.parametrize(
    ("route", "body", "error"),
    [
        ("/ask", QUESTION, LLMUnavailable("no LLM provider answered")),
        ("/classify", {"description": DESCRIPTION}, ClassificationError("no valid classification")),
    ],
    ids=["ask", "classify"],
)
def test_model_failures_return_503(route, body, error):
    """No model answered in time, or no valid classification: 503 with the reason."""
    response = client(FakeClassifier(error), ScriptedLLM(error)).post(route, json=body)

    assert (response.status_code, response.json()["detail"]) == (503, str(error))


def test_one_deadline_per_request():
    """Each request gets one deadline, REQUEST_BUDGET after it starts, for all its calls (R5)."""
    llm, classifier = ScriptedLLM(REPLY), FakeClassifier()
    api = client(classifier, llm)

    start = time.monotonic()
    api.post("/ask", json=QUESTION)
    api.post("/classify", json={"description": DESCRIPTION})
    deadlines = [llm.calls[0]["deadline"], classifier.calls[0][1]]

    assert all(start + REQUEST_BUDGET <= d <= time.monotonic() + REQUEST_BUDGET for d in deadlines)


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
