import numpy as np
import pytest

from actwise.retrieval.dense import DenseRetriever, EmbeddingCache, Passage, build_store
from actwise.retrieval.embedders import l2_normalize
from actwise.retrieval.stores import NumpyStore

VOCAB = ["erasure", "ban", "risk", "fine"]


class CountingEmbedder:
    """Bag-of-words over a tiny vocabulary; counts how many texts it embedded."""

    config = {"model": "counting", "vocab": VOCAB}

    def __init__(self):
        """Start with no text embedded."""
        self.calls = 0

    def encode(self, texts, kind="passage"):
        """Count each vocabulary word in each text (+0.01, so no row is all zeros)."""
        self.calls += len(texts)
        counts = [[t.lower().count(word) + 0.01 for word in VOCAB] for t in texts]
        return l2_normalize(np.array(counts, dtype=np.float32))


PASSAGES = [
    Passage("GDPR-Art17-1", "en", "Right to erasure: erasure of personal data"),
    Passage("AIA-Art5-1", "en", "The ban on prohibited practices"),
    Passage("AIA-Art9-1", "en", "Risk management system for high risk systems"),
    Passage("GDPR-Art83-5", "en", "Administrative fine up to 4 %"),
    Passage("AIA-Art5-1", "fr", "Interdiction : ban des pratiques"),
]


def test_store_returns_best_matches_first():
    """Search returns the `k` most similar keys with their scores, best first."""
    store = NumpyStore(["a", "b", "c"], np.eye(3, dtype=np.float32))

    assert store.search(np.array([0.1, 0.9, 0.0]), k=2) == [
        ("b", pytest.approx(0.9)),
        ("a", pytest.approx(0.1)),
    ]


def test_store_needs_one_key_per_vector():
    """A store with fewer keys than vectors is refused."""
    with pytest.raises(ValueError):
        NumpyStore(["a"], np.eye(2, dtype=np.float32))


def test_dense_retriever_finds_the_right_article():
    """A question about erasure retrieves the erasure article first."""
    embedder = CountingEmbedder()
    retriever = DenseRetriever(PASSAGES, embedder, build_store(PASSAGES, embedder, cache_root=None))

    hits = retriever.search("right to erasure", top_k=2)

    assert hits[0].id == "GDPR-Art17-1"
    assert hits[0].score >= hits[1].score


def test_cache_embeds_each_passage_once(tmp_path):
    """A second build reads the cache instead of embedding again."""
    embedder = CountingEmbedder()

    build_store(PASSAGES, embedder, tmp_path, shard_size=2)
    build_store(PASSAGES, embedder, tmp_path, shard_size=2)

    assert embedder.calls == len(PASSAGES)


def test_cache_resumes_after_an_interrupted_run(tmp_path):
    """A partly filled cache lists its missing shards and loads only once they are filled."""
    texts = [p.text for p in PASSAGES]
    cache = EmbeddingCache(tmp_path, CountingEmbedder.config, texts, shard_size=2)

    cache.fill(CountingEmbedder(), shards=[0])
    assert cache.missing() == [1, 2]
    with pytest.raises(RuntimeError):
        cache.load()

    cache.fill(CountingEmbedder())
    assert cache.missing() == []
    assert cache.load().shape == (len(texts), len(VOCAB))


def test_changed_text_or_model_gets_a_fresh_cache(tmp_path):
    """Another model or an edited text gets a new cache folder; identical inputs reuse it."""
    texts = [p.text for p in PASSAGES]
    base = EmbeddingCache(tmp_path, {"model": "a"}, texts)

    assert EmbeddingCache(tmp_path, {"model": "b"}, texts).dir != base.dir
    assert EmbeddingCache(tmp_path, {"model": "a"}, [*texts[:-1], "edited"]).dir != base.dir
    assert EmbeddingCache(tmp_path, {"model": "a"}, list(texts)).dir == base.dir
