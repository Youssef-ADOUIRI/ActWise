"""Cross-encoder reranking: read the query and each candidate together, then reorder."""

from __future__ import annotations

from typing import Any, Protocol

# Hub name and pinned commit (main on 2026-10-20; it ships model.safetensors, so no redirect).
BGE_RERANKER = ("BAAI/bge-reranker-v2-m3", "953dc6f6f85a1b2dbfca4c34a2796e7dde08d41e")


class Reranker(Protocol):
    config: dict[str, Any]

    def score(self, query: str, texts: list[str]) -> list[float]:
        """One relevance score per text; higher is better."""
        ...


class CrossEncoderReranker:
    """Local profile: a sentence-transformers cross-encoder (needs torch)."""

    def __init__(
        self, name: str, revision: str | None = None, max_len: int = 512, batch_size: int = 8
    ):
        """Record the settings in `config`; the model loads on the first `score()`."""
        self.name, self.revision = name, revision
        self.max_len, self.batch_size = max_len, batch_size
        self.config = {"model": name, "revision": revision, "max_len": max_len}
        self._model: Any = None

    def score(self, query: str, texts: list[str]) -> list[float]:
        """Score each (query, text) pair with the cross-encoder."""
        if self._model is None:
            from sentence_transformers import CrossEncoder  # heavy: imported only when used

            self._model = CrossEncoder(self.name, revision=self.revision, max_length=self.max_len)
        pairs = [(query, text) for text in texts]
        scores = self._model.predict(pairs, batch_size=self.batch_size, show_progress_bar=False)
        return [float(score) for score in scores]
