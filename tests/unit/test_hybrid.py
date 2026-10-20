from actwise.retrieval.bm25 import BM25
from actwise.retrieval.dense import DenseRetriever, build_store
from actwise.retrieval.hybrid import HybridRetriever
from actwise.retrieval.passages import Passage
from tests.unit.toys import PASSAGES, CountingEmbedder


def hybrid(cache, reranker=None, rerank_pool=20):
    """A hybrid retriever over the toy passages, with the toy embedder."""
    embedder = CountingEmbedder()
    dense = DenseRetriever(PASSAGES, embedder, build_store(PASSAGES, embedder, cache))
    return HybridRetriever(dense, BM25(PASSAGES), reranker, k_each=5, rerank_pool=rerank_pool)


class PrefersFines:
    """Fake reranker that only likes the passage about fines."""

    config = {"model": "prefers-fines"}

    def score(self, query, texts):
        """1 for the fines passage, 0 for everything else."""
        return [1.0 if "fine" in text else 0.0 for text in texts]


def test_hybrid_end_to_end(tmp_path):
    """With a toy embedder, "right to erasure" returns GDPR-Art17 first."""
    hits = hybrid(tmp_path).search("right to erasure", top_k=3)

    assert hits[0].id == "GDPR-Art17-1"
    assert len({hit.key for hit in hits}) == 3


def test_reranker_reorders(tmp_path):
    """A fake reranker that prefers one chunk changes the order; the tail keeps its order."""
    plain = [hit.key for hit in hybrid(tmp_path).search("right to erasure", top_k=5)]
    reranked = hybrid(tmp_path, PrefersFines()).search("right to erasure", top_k=5)
    small_pool = hybrid(tmp_path, PrefersFines(), rerank_pool=2).search("right to erasure", 5)

    assert plain[0] == "GDPR-Art17-1@en"
    assert reranked[0].key == "GDPR-Art83-5@en"
    assert [hit.key for hit in small_pool][2:] == plain[2:]


def test_binding_first_ranks_recitals_after_articles(tmp_path):
    """A recital that matches the question best still comes after every article."""
    passages = [*PASSAGES, Passage("GDPR-Rec65", "en", "Right to erasure")]
    embedder = CountingEmbedder()
    dense = DenseRetriever(passages, embedder, build_store(passages, embedder, tmp_path))

    plain = HybridRetriever(dense, BM25(passages), k_each=6).search("right to erasure", 6)
    binding = HybridRetriever(dense, BM25(passages), k_each=6, binding_first=True)

    hits = binding.search("right to erasure", 6)
    assert plain[0].id == "GDPR-Rec65"
    assert hits[0].id == "GDPR-Art17-1" and hits[-1].id == "GDPR-Rec65"
