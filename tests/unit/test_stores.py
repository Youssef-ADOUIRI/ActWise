import logging
import os
import uuid

import httpx
import numpy as np
import pytest

from actwise.retrieval.stores import FallbackStore, NumpyStore, QdrantStore
from tests.unit.toys import PASSAGES, CountingEmbedder

PAYLOADS = [p.payload for p in PASSAGES]
VECTORS = CountingEmbedder().encode([p.text for p in PASSAGES])


def test_numpy_store_returns_best_matches_first():
    """Search returns the `k` most similar keys with their scores, best first."""
    store = NumpyStore([{"key": "a"}, {"key": "b"}, {"key": "c"}], np.eye(3, dtype=np.float32))

    assert store.search(np.array([0.1, 0.9, 0.0]), k=2) == [
        ("b", pytest.approx(0.9)),
        ("a", pytest.approx(0.1)),
    ]


def test_numpy_store_needs_one_payload_per_vector():
    """A store with fewer payloads than vectors is refused."""
    with pytest.raises(ValueError):
        NumpyStore([{"key": "a"}], np.eye(2, dtype=np.float32))


def test_numpy_store_where_keeps_matching_payloads():
    """`where` drops every passage whose payload differs."""
    store = NumpyStore(PAYLOADS, VECTORS)

    keys = [key for key, _ in store.search(VECTORS[0], k=5, where={"law": "gdpr"})]

    assert keys == ["GDPR-Art17-1@en", "GDPR-Art83-5@en"]


class BrokenStore:
    """A primary store whose server is down."""

    def search(self, vector, k, where=None):
        """Fail like a refused connection."""
        raise ConnectionError("qdrant is down")


def test_store_failover(caplog):
    """A primary store that raises is replaced by the NumPy store, and the event is logged."""
    fallback = NumpyStore(PAYLOADS, VECTORS)

    with caplog.at_level(logging.WARNING):
        results = FallbackStore(BrokenStore(), fallback).search(VECTORS[0], k=2)

    assert results == fallback.search(VECTORS[0], k=2)
    assert "qdrant is down" in caplog.text


def test_point_ids_keep_languages_apart():
    """EN and FR share a chunk id but get two points, and re-indexing reuses them (R1)."""
    en, fr = QdrantStore.point_id("AIA-Art5-1@en"), QdrantStore.point_id("AIA-Art5-1@fr")

    assert en != fr
    assert en == QdrantStore.point_id("AIA-Art5-1@en")


@pytest.fixture(params=["memory", pytest.param("server", marks=pytest.mark.integration)])
def qdrant(request):
    """Qdrant in process (always) and the Docker server (when one is running)."""
    qdrant_client = pytest.importorskip("qdrant_client")
    if request.param == "memory":
        yield qdrant_client.QdrantClient(":memory:")
        return
    url = os.environ.get("QDRANT_URL", "http://localhost:6333")
    try:
        httpx.get(f"{url}/readyz", timeout=2).raise_for_status()
    except httpx.HTTPError:
        pytest.skip("no Qdrant server: run `docker compose up -d qdrant`")
    client = qdrant_client.QdrantClient(url=url)
    yield client
    client.close()


def test_gdpr_filter(qdrant):
    """A query filtered on law == "gdpr" returns no AI Act chunks; re-indexing adds no points."""
    store = QdrantStore(qdrant, f"actwise_test_{uuid.uuid4().hex[:8]}")
    try:
        store.index(PAYLOADS, VECTORS)
        store.index(PAYLOADS, VECTORS)

        everything = store.search(VECTORS[1], k=10)
        gdpr_only = store.search(VECTORS[1], k=10, where={"law": "gdpr"})

        assert len(everything) == len(PASSAGES)
        assert {key for key, _ in everything} > {key for key, _ in gdpr_only}
        assert [key.split("-")[0] for key, _ in gdpr_only] == ["GDPR", "GDPR"]
    finally:
        qdrant.delete_collection(store.collection)
