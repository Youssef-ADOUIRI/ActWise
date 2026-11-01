"""The retrieval systems of docs/ablations.md, by name: the evals and the API build them here."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Protocol

from actwise.retrieval.bm25 import BM25
from actwise.retrieval.dense import CACHE_DIR, DenseRetriever, build_store
from actwise.retrieval.embedders import BGE_M3, SentenceTransformerEmbedder
from actwise.retrieval.hybrid import HybridRetriever
from actwise.retrieval.naive import MAX_WORDS, OVERLAP, naive_passages
from actwise.retrieval.passages import Hit, Passage, chunk_passages
from actwise.retrieval.rerank import BGE_RERANKER, CrossEncoderReranker

SERVED = "hybrid-binding"  # system E: what the API and the classifier search with


class Retriever(Protocol):
    config: dict[str, Any]

    def search(self, query: str, top_k: int = 5) -> list[Hit]:
        """The `top_k` best passages for the query, best first."""
        ...


def dense(passages: list[Passage]) -> DenseRetriever:
    """Cosine search with the pinned BGE-M3 over cached passage vectors."""
    embedder = SentenceTransformerEmbedder(*BGE_M3)
    return DenseRetriever(passages, embedder, build_store(passages, embedder, CACHE_DIR))


def hybrid(rerank: bool = False, binding_first: bool = False) -> HybridRetriever:
    """Dense and BM25 over the structure-aware chunks, fused with RRF."""
    passages = chunk_passages()
    reranker = CrossEncoderReranker(*BGE_RERANKER) if rerank else None
    return HybridRetriever(dense(passages), BM25(passages), reranker, binding_first=binding_first)


@dataclass(frozen=True)
class System:
    description: str
    build: Callable[[], Retriever]


CHUNKS = "structure-aware chunks with their headers"
SYSTEMS = {
    "baseline": System(
        f"Baseline: fixed {MAX_WORDS}-word windows ({OVERLAP} shared) ignoring "
        "structure, dense BGE-M3, cosine similarity, no rerank",
        lambda: dense(naive_passages()),
    ),
    "dense": System(f"A: {CHUNKS}, dense BGE-M3, no rerank", lambda: dense(chunk_passages())),
    "bm25": System(f"B: {CHUNKS}, BM25 only, no rerank", lambda: BM25(chunk_passages())),
    "hybrid": System(f"C: {CHUNKS}, dense BGE-M3 + BM25 fused with RRF, no rerank", hybrid),
    "hybrid-rerank": System(
        f"D: {CHUNKS}, dense BGE-M3 + BM25 fused with RRF, top 20 reranked by bge-reranker-v2-m3",
        lambda: hybrid(rerank=True),
    ),
    "hybrid-binding": System(
        "E: as C, with articles and annexes ranked before recitals",
        lambda: hybrid(binding_first=True),
    ),
    "hybrid-rerank-binding": System(
        "F: as D, with articles and annexes ranked before recitals",
        lambda: hybrid(rerank=True, binding_first=True),
    ),
}
