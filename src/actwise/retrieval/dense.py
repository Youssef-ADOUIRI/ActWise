"""Dense retrieval: embed the passages once (cached on disk), then cosine search."""

from __future__ import annotations

import hashlib
import json
import logging
import math
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np

from actwise.retrieval.embedders import Embedder
from actwise.retrieval.stores import NumpyStore

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class Passage:
    """A text to retrieve. `id` is the language-free chunk id that metrics and citations use."""

    id: str
    lang: str
    text: str

    @property
    def key(self) -> str:
        return f"{self.id}@{self.lang}"


@dataclass(frozen=True)
class Hit:
    id: str
    lang: str
    text: str
    score: float


class EmbeddingCache:
    """Passage vectors saved in shards on disk, so a slow CPU run can stop and resume.

    The folder name hashes the embedder config and every text: change either
    and the cache starts fresh instead of serving stale vectors.
    """

    def __init__(self, root: Path, config: dict[str, Any], texts: list[str], shard_size: int = 64):
        blob = json.dumps({"config": config, "shard_size": shard_size, "texts": texts})
        self.dir = root / hashlib.sha256(blob.encode("utf-8")).hexdigest()[:16]
        self.texts, self.shard_size = texts, shard_size

    @property
    def n_shards(self) -> int:
        return math.ceil(len(self.texts) / self.shard_size)

    def path(self, shard: int) -> Path:
        return self.dir / f"{shard:05d}.npy"

    def missing(self) -> list[int]:
        return [shard for shard in range(self.n_shards) if not self.path(shard).exists()]

    def fill(self, embedder: Embedder, shards: Iterable[int] | None = None) -> None:
        self.dir.mkdir(parents=True, exist_ok=True)
        todo = self.missing() if shards is None else list(shards)
        for done, shard in enumerate(todo, start=1):
            texts = self.texts[shard * self.shard_size : (shard + 1) * self.shard_size]
            tmp = self.dir / f"{shard:05d}.tmp.npy"
            np.save(tmp, embedder.encode(texts, kind="passage"))
            tmp.replace(self.path(shard))  # atomic: a killed run never leaves half a shard
            log.info("embedded shard %d/%d (%d to go)", done, len(todo), len(todo) - done)

    def load(self) -> np.ndarray:
        if missing := self.missing():
            raise RuntimeError(f"{len(missing)} of {self.n_shards} shards are not embedded yet")
        return np.concatenate([np.load(self.path(shard)) for shard in range(self.n_shards)])


def build_store(
    passages: list[Passage], embedder: Embedder, cache_root: Path | None, shard_size: int = 64
) -> NumpyStore:
    """Embed every passage (reusing the cache under `cache_root` when given)."""
    texts = [p.text for p in passages]
    if cache_root is None:
        vectors = embedder.encode(texts, kind="passage")
    else:
        cache = EmbeddingCache(cache_root, embedder.config, texts, shard_size)
        cache.fill(embedder)
        vectors = cache.load()
    return NumpyStore([p.key for p in passages], vectors)


class DenseRetriever:
    def __init__(self, passages: list[Passage], embedder: Embedder, store: NumpyStore):
        self.passages = {p.key: p for p in passages}
        self.embedder, self.store = embedder, store

    def search(self, query: str, top_k: int = 5) -> list[Hit]:
        vector = self.embedder.encode([query], kind="query")[0]
        hits = []
        for key, score in self.store.search(vector, top_k):
            passage = self.passages[key]
            hits.append(Hit(passage.id, passage.lang, passage.text, score))
        return hits
