"""Embedders behind one interface: encode(texts, kind) -> L2-normalised float32 matrix.

`kind` is "query" or "passage" because some models (e5, BGE v1.5) want a
prefix on one side; BGE-M3 needs none. `config` names the vector space, so a
cache built with another model or setting is never reused by mistake.
"""

from __future__ import annotations

from typing import Any, Protocol

import numpy as np


class Embedder(Protocol):
    config: dict[str, Any]

    def encode(self, texts: list[str], kind: str = "passage") -> np.ndarray: ...


def l2_normalize(x: np.ndarray) -> np.ndarray:
    return x / np.clip(np.linalg.norm(x, axis=1, keepdims=True), 1e-12, None)


class SentenceTransformerEmbedder:
    """Local profile: BGE-M3, multilingual-e5 or a fine-tuned model (needs torch)."""

    def __init__(
        self,
        name: str,
        max_len: int = 512,
        batch_size: int = 8,
        query_prefix: str = "",
        passage_prefix: str = "",
    ):
        from sentence_transformers import SentenceTransformer  # heavy: imported only when used

        self.model = SentenceTransformer(name)
        self.model.max_seq_length = max_len
        self.batch_size = batch_size
        self.prefix = {"query": query_prefix, "passage": passage_prefix}
        self.config = {"model": name, "max_len": max_len, "prefix": self.prefix}

    def encode(self, texts: list[str], kind: str = "passage") -> np.ndarray:
        vectors = self.model.encode(
            [self.prefix[kind] + text for text in texts],
            batch_size=self.batch_size,
            show_progress_bar=False,
        )
        return l2_normalize(np.asarray(vectors, dtype=np.float32))
