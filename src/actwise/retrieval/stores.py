"""Vector stores behind one `search()`: NumPy (exact, in process), Qdrant, and a fallback pair."""

from __future__ import annotations

import logging
import uuid
from typing import Any, Protocol

import numpy as np

log = logging.getLogger(__name__)

Where = dict[str, str]  # payload field -> required value, such as {"law": "gdpr"}


class Store(Protocol):
    """Anything that returns the storage keys closest to a vector, best first."""

    def search(
        self, vector: np.ndarray, k: int, where: Where | None = None
    ) -> list[tuple[str, float]]:
        """The `k` best (key, score) pairs whose payload matches `where`."""
        ...


class NumpyStore:
    """Exact cosine search over L2-normalised vectors: a few thousand passages take ~1 ms."""

    def __init__(self, payloads: list[dict[str, str]], vectors: np.ndarray):
        """One payload per vector row; each payload holds the storage `key`."""
        if len(payloads) != len(vectors):
            raise ValueError(f"{len(payloads)} payloads for {len(vectors)} vectors")
        self.payloads, self.vectors = payloads, vectors.astype(np.float32)

    def search(
        self, vector: np.ndarray, k: int, where: Where | None = None
    ) -> list[tuple[str, float]]:
        """The `k` keys with the highest dot product (cosine for unit vectors), best first."""
        scores = self.vectors @ vector.astype(np.float32)
        rows = np.argsort(-scores, kind="stable").tolist()  # stable: ties keep corpus order
        if where:
            rows = [i for i in rows if all(self.payloads[i][f] == v for f, v in where.items())]
        return [(self.payloads[i]["key"], float(scores[i])) for i in rows[:k]]


class QdrantStore:
    """Vectors in a Qdrant collection, with the same `search()` as `NumpyStore`."""

    def __init__(self, client: Any, collection: str):
        """Use `client` (a local or remote `QdrantClient`) and one collection per embedder."""
        self.client, self.collection = client, collection

    @staticmethod
    def point_id(key: str) -> str:
        """UUID from the storage key: re-indexing overwrites, and FR never overwrites EN (R1)."""
        return str(uuid.uuid5(uuid.NAMESPACE_URL, key))

    def index(
        self, payloads: list[dict[str, str]], vectors: np.ndarray, batch_size: int = 256
    ) -> None:
        """Create the collection if needed, then upsert one point per vector."""
        from qdrant_client.models import Distance, PointStruct, VectorParams

        if not self.client.collection_exists(self.collection):
            config = VectorParams(size=vectors.shape[1], distance=Distance.COSINE)
            self.client.create_collection(self.collection, vectors_config=config)
        points = [
            PointStruct(id=self.point_id(p["key"]), vector=v.tolist(), payload=p)
            for p, v in zip(payloads, vectors, strict=True)
        ]
        for start in range(0, len(points), batch_size):
            self.client.upsert(self.collection, points=points[start : start + batch_size])

    def search(
        self, vector: np.ndarray, k: int, where: Where | None = None
    ) -> list[tuple[str, float]]:
        """The `k` closest points whose payload matches `where`, as (key, score)."""
        from qdrant_client.models import FieldCondition, Filter, MatchValue

        must: list[Any] = [
            FieldCondition(key=f, match=MatchValue(value=v)) for f, v in (where or {}).items()
        ]
        result = self.client.query_points(
            self.collection,
            query=vector.tolist(),
            limit=k,
            query_filter=Filter(must=must) if must else None,
            with_payload=True,
        )
        return [(point.payload["key"], point.score) for point in result.points]


class FallbackStore:
    """The primary store, or the fallback when the primary fails; each failure is logged."""

    def __init__(self, primary: Store, fallback: Store):
        """Usually Qdrant first, then an in-process `NumpyStore` with the same vectors."""
        self.primary, self.fallback = primary, fallback

    def search(
        self, vector: np.ndarray, k: int, where: Where | None = None
    ) -> list[tuple[str, float]]:
        """Ask the primary; on any error, log it and ask the fallback."""
        try:
            return self.primary.search(vector, k, where)
        except Exception as exc:  # network and client errors differ per client
            log.warning("primary store failed, using the fallback: %r", exc)
            return self.fallback.search(vector, k, where)
