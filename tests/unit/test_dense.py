import pytest

from actwise.retrieval.dense import DenseRetriever, EmbeddingCache, build_store
from tests.unit.toys import PASSAGES, VOCAB, CountingEmbedder

TEXTS = [p.text for p in PASSAGES]


def test_dense_retriever_finds_the_right_article(tmp_path):
    """A question about erasure retrieves the erasure article first."""
    embedder = CountingEmbedder()
    retriever = DenseRetriever(PASSAGES, embedder, build_store(PASSAGES, embedder, tmp_path))

    hits = retriever.search("right to erasure", top_k=2)

    assert hits[0].id == "GDPR-Art17-1"
    assert hits[0].score >= hits[1].score


def test_where_filters_the_results(tmp_path):
    """`where` keeps only the passages whose payload matches."""
    embedder = CountingEmbedder()
    retriever = DenseRetriever(PASSAGES, embedder, build_store(PASSAGES, embedder, tmp_path))

    hits = retriever.search("ban", top_k=5, where={"lang": "fr"})

    assert [hit.key for hit in hits] == ["AIA-Art5-1@fr"]


def test_cache_embeds_each_text_once(tmp_path):
    """A second build reads the cache instead of embedding again."""
    embedder = CountingEmbedder()

    build_store(PASSAGES, embedder, tmp_path, shard_size=2)
    build_store(PASSAGES, embedder, tmp_path, shard_size=2)

    assert embedder.calls == len(PASSAGES)


def test_cache_resumes_after_an_interrupted_run(tmp_path):
    """A partly filled cache reports what is left and loads only once everything is there."""
    cache = EmbeddingCache(tmp_path, CountingEmbedder.config, shard_size=2)

    assert cache.fill(CountingEmbedder(), TEXTS, max_shards=1) == len(TEXTS) - 2
    with pytest.raises(RuntimeError):
        cache.load(TEXTS)

    assert cache.fill(CountingEmbedder(), TEXTS) == 0
    assert cache.load(TEXTS).shape == (len(TEXTS), len(VOCAB))


def test_an_edited_text_only_embeds_itself(tmp_path):
    """Changing one passage costs one new vector; the others stay cached."""
    cache = EmbeddingCache(tmp_path, CountingEmbedder.config)
    cache.fill(CountingEmbedder(), TEXTS)
    embedder = CountingEmbedder()

    cache.fill(embedder, [*TEXTS[:-1], "edited ban"])

    assert embedder.calls == 1


def test_another_model_gets_another_folder(tmp_path):
    """The folder depends on the embedder config only, not on the order of its keys."""
    base = EmbeddingCache(tmp_path, {"model": "a", "revision": "1"})

    assert EmbeddingCache(tmp_path, {"model": "b", "revision": "1"}).dir != base.dir
    assert EmbeddingCache(tmp_path, {"revision": "1", "model": "a"}).dir == base.dir
