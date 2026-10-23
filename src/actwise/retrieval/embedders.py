"""Embedders behind one interface: encode(texts, kind) -> L2-normalised float32 matrix.

`kind` is "query" or "passage" because some models (e5, BGE v1.5) want a
prefix on one side; BGE-M3 needs none. `config` names the vector space, so a
cache built with another model or setting is never reused by mistake.
"""

from __future__ import annotations

from typing import Any, Protocol

import numpy as np

# Hub name and pinned commit. 9a0624b is the bot-made safetensors variant of main (5617a9f):
# same weights, but it loads without pickle and without transformers' silent PR redirect.
BGE_M3 = ("BAAI/bge-m3", "9a0624b896d81da7492a910ffa53731274b6cf3d")


class Embedder(Protocol):
    config: dict[str, Any]

    def encode(self, texts: list[str], kind: str = "passage") -> np.ndarray:
        """One L2-normalised float32 row per text; `kind` is "query" or "passage"."""
        ...

    def unload(self) -> None:
        """Free the model's memory; the next `encode()` loads it again."""
        ...


def l2_normalize(x: np.ndarray) -> np.ndarray:
    """Scale each row to unit length, so a dot product is a cosine similarity."""
    return x / np.clip(np.linalg.norm(x, axis=1, keepdims=True), 1e-12, None)


class SentenceTransformerEmbedder:
    """Local profile: BGE-M3, multilingual-e5 or a fine-tuned model (needs torch)."""

    def __init__(
        self,
        name: str,
        revision: str | None = None,
        max_len: int = 512,
        batch_size: int = 8,
        query_prefix: str = "",
        passage_prefix: str = "",
    ):
        """Record the settings in `config`; the model loads on the first `encode()`."""
        # Pin `revision` (a Hub commit hash) so reported numbers stay reproducible.
        self.name, self.revision = name, revision
        self.max_len, self.batch_size = max_len, batch_size
        self.prefix = {"query": query_prefix, "passage": passage_prefix}
        self.config = {
            "model": name,
            "revision": revision,
            "max_len": max_len,
            "prefix": self.prefix,
        }
        self._model: Any = None

    def encode(self, texts: list[str], kind: str = "passage") -> np.ndarray:
        """Add the prefix for `kind`, embed in batches and L2-normalise the result."""
        if self._model is None:  # a run served entirely from the cache never loads it
            from sentence_transformers import SentenceTransformer  # heavy: imported only when used

            self._model = SentenceTransformer(self.name, revision=self.revision)
            self._model.max_seq_length = self.max_len
        vectors = self._model.encode(
            [self.prefix[kind] + text for text in texts],
            batch_size=self.batch_size,
            show_progress_bar=False,
        )
        return l2_normalize(np.asarray(vectors, dtype=np.float32))

    def unload(self) -> None:
        """Free the model's memory; the next `encode()` loads it again."""
        self._model = None
