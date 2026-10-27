"""The HTTP API. The pipelines are injected, so the tests run it with fakes; `app.py` wires it."""

from __future__ import annotations

import logging
import os
import secrets
import time
from collections.abc import Callable
from typing import Annotated, Any, Literal, Protocol

from fastapi import Depends, FastAPI, Header, HTTPException, Query, Request, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from actwise.agent.classifier import ClassificationError, ClassifyOutcome
from actwise.agent.schemas import DISCLAIMER, Classification
from actwise.api.guards import DailyCap
from actwise.generation.rag import AskResult, Search, sources_of
from actwise.ingest.files import UnsupportedFile, extract_text
from actwise.llm.wrappers import LLMUnavailable

log = logging.getLogger(__name__)

REQUEST_BUDGET = 50.0  # seconds for every model call of one request, under Cloud Run's 60 s (R5)
MIN_DESCRIPTION, MAX_DESCRIPTION = 20, 8_000  # characters, for /classify and /upload alike
MAX_UPLOAD = 2_000_000  # bytes
MAX_TOP_K, SNIPPET = 10, 500  # /search: passages, and characters of each

Ask = Callable[[str, str, float], AskResult]  # (question, lang, deadline)
Classify = Callable[[str, float], ClassifyOutcome]  # (description, deadline)


class Register(Protocol):
    """Where classifications are logged: the Google Sheets register of step 11."""

    def log(self, description: str, result: Classification) -> None:
        """Record one classification."""
        ...


class AskIn(BaseModel):
    """A question on the AI Act or the GDPR, and the language of the answer."""

    question: str = Field(min_length=3, max_length=1000)
    lang: Literal["en", "fr"] = "en"


class ClassifyIn(BaseModel):
    """The description of the AI system to classify."""

    description: str = Field(min_length=MIN_DESCRIPTION, max_length=MAX_DESCRIPTION)


def create_app(
    ask: Ask,
    classify: Classify,
    search: Search,
    register: Register | None = None,
    api_key: str | None = None,
    daily_cap: int = 200,
) -> FastAPI:
    """The API around these pipelines. With `api_key`, every route but /health needs X-API-Key."""
    app = FastAPI(title="ActWise", version=os.environ.get("APP_VERSION", "dev"))
    cap = DailyCap(daily_cap)

    def check_key(x_api_key: Annotated[str | None, Header()] = None) -> None:
        """401 unless the request carries the API key, when one is set."""
        if api_key and not secrets.compare_digest((x_api_key or "").encode(), api_key.encode()):
            raise HTTPException(401, "invalid API key")

    def start_model_request() -> float:
        """Count the request against the daily cap (429 past it); return its deadline (R5)."""
        if not cap.allow():
            raise HTTPException(429, "the demo's daily quota is used up, try again tomorrow")
        return time.monotonic() + REQUEST_BUDGET

    def classified(description: str) -> dict[str, Any]:
        """The classification with the notice; a failing register is logged, not raised."""
        result = classify(description, start_model_request()).result
        if register is not None:
            try:
                register.log(description, result)
            except Exception:  # a register outage must not lose the user's answer
                log.warning("the register failed", exc_info=True)
        return result.model_dump() | {"disclaimer": DISCLAIMER}

    @app.exception_handler(LLMUnavailable)
    @app.exception_handler(ClassificationError)
    async def unavailable(request: Request, exc: Exception) -> JSONResponse:
        """503: no model answered before the deadline, or no valid classification came back."""
        log.warning("503: %r", exc)
        return JSONResponse({"detail": str(exc)}, status_code=503)

    keyed = [Depends(check_key)]

    @app.get("/health")
    def health() -> dict[str, str]:
        """Liveness, and the version that is running."""
        return {"status": "ok", "version": app.version}

    @app.get("/search", dependencies=keyed)
    def search_passages(
        q: Annotated[str, Query(min_length=1, max_length=1000)], top_k: int = 5
    ) -> list[dict[str, Any]]:
        """The best passages and their scores: no model call, so no daily cap."""
        hits = search(q, max(1, min(top_k, MAX_TOP_K)))
        return [
            source | {"text": source["text"][:SNIPPET], "score": hit.score}
            for source, hit in zip(sources_of(hits, "en"), hits, strict=True)
        ]

    @app.post("/ask", dependencies=keyed)
    def answer(body: AskIn) -> dict[str, Any]:
        """A cited answer or a refusal, with the passages it was drawn from."""
        result = ask(body.question, body.lang, start_model_request())
        return {
            "answer": result.answer,
            "refused": result.refused,
            "reason": result.reason,
            "citations": result.citations,
            "sources": result.sources,
            "model": result.reply.model if result.reply else None,
            "disclaimer": DISCLAIMER,
        }

    @app.post("/classify", dependencies=keyed)
    def classify_text(body: ClassifyIn) -> dict[str, Any]:
        """The AI Act risk tier, with reasons, citations and follow-up questions."""
        return classified(body.description)

    @app.post("/upload", dependencies=keyed)
    def classify_file(file: UploadFile) -> dict[str, Any]:
        """Classify a description sent as a .txt, .md, .pdf or .docx file of up to 2 MB."""
        data = file.file.read(MAX_UPLOAD + 1)
        if len(data) > MAX_UPLOAD:
            raise HTTPException(413, "the file is over 2 MB")
        try:
            text = extract_text(file.filename or "", data, MAX_DESCRIPTION)
        except UnsupportedFile as exc:
            raise HTTPException(415, str(exc)) from exc
        if len(text) < MIN_DESCRIPTION:
            raise HTTPException(422, "no readable text in the file")
        return classified(text)

    return app
