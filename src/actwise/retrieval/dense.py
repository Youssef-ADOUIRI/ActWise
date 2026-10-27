"""Dense retrieval: embed each passage text once (cached on disk), then cosine search."""

from __future__ import annotations

import hashlib
import json
import logging
from pathlib import Path
from typing import Any

import numpy as np

from actwise.retrieval.embedders import Embedder
from actwise.retrieval.passages import Hit, Passage, to_hit
from actwise.retrieval.stores import NumpyStore, Store, Where

log = logging.getLogger(__name__)

CACHE_DIR = Path(".cache/embeddings")


def text_hash(text: str) -> str:
    """SHA-256 of a text: its key in the embedding cache."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class EmbeddingCache:
    """Passage vectors on disk, keyed by text, so each text is embedded once per model.

    The folder name hashes the embedder config, so another model or setting never
    serves these vectors. Each shard stores the hashes of its texts next to their
    vectors and is written atomically: a slow CPU run can stop and resume, and an
    edited passage only costs its own vector.
    """

    def __init__(self, root: Path, config: dict[str, Any], shard_size: int = 64):
        """Point at the folder for this embedder config; embed nothing until `fill()`."""
        name = text_hash(json.dumps(config, sort_keys=True))[:16]
        self.dir, self.shard_size = root / name, shard_size

    def _shards(self) -> list[Path]:
        """Every complete shard file, in a fixed order."""
        return sorted(self.dir.glob("*.npz"))

    def hashes(self) -> set[str]:
        """Hashes of every text embedded so far."""
        found: set[str] = set()
        for path in self._shards():
            with np.load(path) as shard:
                found.update(shard["keys"].tolist())
        return found

    def missing(self, texts: list[str]) -> list[str]:
        """Texts without a vector yet, each once, in order."""
        known = self.hashes()
        return [text for text in dict.fromkeys(texts) if text_hash(text) not in known]

    def fill(self, embedder: Embedder, texts: list[str], max_shards: int | None = None) -> int:
        """Embed the missing texts one shard at a time; return how many are still missing."""
        todo = self.missing(texts)
        batches = [todo[i : i + self.shard_size] for i in range(0, len(todo), self.shard_size)]
        self.dir.mkdir(parents=True, exist_ok=True)
        for done, batch in enumerate(batches[:max_shards], start=1):
            hashes = [text_hash(text) for text in batch]
            path = self.dir / f"{text_hash(''.join(hashes))[:16]}.npz"
            tmp = path.with_suffix(".tmp")
            with tmp.open("wb") as f:
                np.savez(f, keys=np.array(hashes), vectors=embedder.encode(batch, kind="passage"))
            tmp.replace(path)  # atomic: a killed run never leaves half a shard
            log.info("embedded shard %d of %d", done, len(batches))
        return len(todo) - sum(len(batch) for batch in batches[:max_shards])

    def load(self, texts: list[str]) -> np.ndarray:
        """Vectors in the order of `texts`; RuntimeError if any text is not embedded yet."""
        found: dict[str, np.ndarray] = {}
        for path in self._shards():
            with np.load(path) as shard:
                found.update(zip(shard["keys"].tolist(), shard["vectors"], strict=True))
        if missing := [text for text in texts if text_hash(text) not in found]:
            raise RuntimeError(f"{len(missing)} of {len(texts)} texts are not embedded yet")
        return np.stack([found[text_hash(text)] for text in texts])


def build_store(
    passages: list[Passage], embedder: Embedder, cache_root: Path, shard_size: int = 64
) -> NumpyStore:
    """Embed every passage, reusing the vectors cached under `cache_root`."""
    texts = [p.text for p in passages]
    cache = EmbeddingCache(cache_root, embedder.config, shard_size)
    cache.fill(embedder, texts)
    return NumpyStore([p.payload for p in passages], cache.load(texts))


class DenseRetriever:
    """Embed the query, then return the closest passages from a vector store."""

    def __init__(self, passages: list[Passage], embedder: Embedder, store: Store):
        """Keep the passages by storage key, so a search can return their text."""
        self.passages = {p.key: p for p in passages}
        self.embedder, self.store = embedder, store
        self.config = {"embedder": embedder.config, "passages": len(passages)}

    def search(self, query: str, top_k: int = 5, where: Where | None = None) -> list[Hit]:
        """The `top_k` passages closest to the query (and matching `where`), best first."""
        vector = self.embedder.encode([query], kind="query")[0]
        results = self.store.search(vector, top_k, where)
        return [to_hit(self.passages[key], score) for key, score in results]
