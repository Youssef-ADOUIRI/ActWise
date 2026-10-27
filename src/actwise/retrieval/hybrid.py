"""Dense + BM25 retrieval fused with RRF, optionally reranked by a cross-encoder."""

from __future__ import annotations

from actwise.ids import is_recital
from actwise.retrieval.bm25 import BM25
from actwise.retrieval.dense import DenseRetriever, bge_m3_retriever
from actwise.retrieval.fusion import rrf
from actwise.retrieval.passages import Hit, chunk_passages, to_hit
from actwise.retrieval.rerank import BGE_RERANKER, CrossEncoderReranker, Reranker


class HybridRetriever:
    """Search both indexes, fuse the two rankings, then optionally rerank the top of the list."""

    def __init__(
        self,
        dense: DenseRetriever,
        bm25: BM25,
        reranker: Reranker | None = None,
        k_each: int = 30,
        rrf_k: int = 60,
        rerank_pool: int = 20,
        binding_first: bool = False,
    ):
        """Take `k_each` hits from each retriever; a reranker reorders the best `rerank_pool`.

        With `binding_first`, articles and annexes come before recitals, which explain
        the law in the words of a question but do not bind (docs/failure_cases.md).
        """
        self.dense, self.bm25, self.reranker = dense, bm25, reranker
        self.k_each, self.rrf_k, self.rerank_pool = k_each, rrf_k, rerank_pool
        self.binding_first = binding_first
        self.config = {
            **dense.config,
            **bm25.config,
            "fusion": {"method": "rrf", "k": rrf_k, "k_each": k_each},
            "reranker": reranker.config if reranker else None,
            "rerank_pool": rerank_pool if reranker else None,
            "binding_first": binding_first,
        }

    def fused(self, query: str) -> list[tuple[str, float]]:
        """Stage 1: the dense and BM25 rankings fused with RRF, as (key, score), best first."""
        dense = [hit.key for hit in self.dense.search(query, self.k_each)]
        sparse = [hit.key for hit in self.bm25.search(query, self.k_each)]
        fused = rrf([dense, sparse], self.rrf_k)
        if self.binding_first:  # stable sort: each group keeps its fused order
            fused.sort(key=lambda item: is_recital(self.dense.passages[item[0]].id))
        return fused

    def reranked(self, query: str, fused: list[tuple[str, float]]) -> list[tuple[str, float]]:
        """Stage 2: the best `rerank_pool` reordered by the reranker, then the rest unchanged."""
        if self.reranker is None:
            return fused
        keys = [key for key, _ in fused[: self.rerank_pool]]
        scores = self.reranker.score(query, [self.dense.passages[key].text for key in keys])
        reranked = sorted(zip(keys, scores, strict=True), key=lambda item: -item[1])
        return reranked + fused[self.rerank_pool :]

    def search(self, query: str, top_k: int = 5) -> list[Hit]:
        """The `top_k` best passages: both stages, one after the other."""
        ranked = self.reranked(query, self.fused(query))
        return [to_hit(self.dense.passages[key], score) for key, score in ranked[:top_k]]


def build_hybrid(rerank: bool = False, binding_first: bool = False) -> HybridRetriever:
    """Dense BGE-M3 and BM25 over the structure-aware chunks; system E is `binding_first`."""
    passages = chunk_passages()
    reranker = CrossEncoderReranker(*BGE_RERANKER) if rerank else None
    dense = bge_m3_retriever(passages)
    return HybridRetriever(dense, BM25(passages), reranker, binding_first=binding_first)
