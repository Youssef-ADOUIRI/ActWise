"""The retrieval systems of docs/ablations.md, by name: the evals and the API build them here.

Row K, the LlamaIndex version of H (step 10), lives in frameworks/ and is added by
evals/run_eval.py, so the product package never imports a framework.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Protocol

from actwise.retrieval.bm25 import BM25
from actwise.retrieval.dense import CACHE_DIR, DenseRetriever, build_store
from actwise.retrieval.embedders import (
    BGE_M3,
    MINILM,
    MINILM_HUB,
    MINILM_MAX_LEN,
    Embedder,
    OnnxEmbedder,
    SentenceTransformerEmbedder,
    hub_snapshot,
)
from actwise.retrieval.hybrid import HybridRetriever
from actwise.retrieval.naive import MAX_WORDS, OVERLAP, naive_passages
from actwise.retrieval.passages import Hit, Passage, chunk_passages
from actwise.retrieval.rerank import BGE_RERANKER, CrossEncoderReranker

SERVED = "hybrid-binding"  # system E: what the API and the classifier search with
MINILM_FT = "models/minilm-ft"  # evals/train_embedder.py writes it (decision 011)
MINILM_FT_INT8 = f"{MINILM_FT}-int8"  # evals/export_onnx.py writes it; MINILM_HUB is its copy


class Retriever(Protocol):
    config: dict[str, Any]

    def search(self, query: str, top_k: int = 5) -> list[Hit]:
        """The `top_k` best passages for the query, best first."""
        ...


def dense(passages: list[Passage], embedder: Embedder | None = None) -> DenseRetriever:
    """Cosine search over cached passage vectors, with the pinned BGE-M3 by default."""
    embedder = embedder or SentenceTransformerEmbedder(*BGE_M3)
    return DenseRetriever(passages, embedder, build_store(passages, embedder, CACHE_DIR))


def hybrid(
    rerank: bool = False, binding_first: bool = False, embedder: Embedder | None = None
) -> HybridRetriever:
    """Dense and BM25 over the structure-aware chunks, fused with RRF."""
    passages = chunk_passages()
    reranker = CrossEncoderReranker(*BGE_RERANKER) if rerank else None
    retriever = dense(passages, embedder)
    return HybridRetriever(retriever, BM25(passages), reranker, binding_first=binding_first)


def minilm(path: str | None = None) -> SentenceTransformerEmbedder:
    """The pinned base MiniLM, or the fine-tuned copy in the local folder `path`."""
    name, revision = (path, None) if path else MINILM
    return SentenceTransformerEmbedder(name, revision, max_len=MINILM_MAX_LEN, batch_size=32)


def minilm_int8() -> OnnxEmbedder:
    """The published int8 MiniLM at its pinned Hub commit: no torch, no local training."""
    return OnnxEmbedder(hub_snapshot(*MINILM_HUB))


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
    "minilm": System(
        f"G: {CHUNKS}, dense multilingual MiniLM-L12 (base), no rerank",
        lambda: dense(chunk_passages(), minilm()),
    ),
    "minilm-ft": System(
        "H: as G, fine-tuned on questions written from train paragraphs",
        lambda: dense(chunk_passages(), minilm(MINILM_FT)),
    ),
    "minilm-ft-int8": System(
        "I: as H, exported to ONNX and quantized to int8 (no torch)",
        lambda: dense(chunk_passages(), minilm_int8()),
    ),
    "hybrid-binding-int8": System(
        "J: as E, with the int8 MiniLM of I instead of BGE-M3",
        lambda: hybrid(binding_first=True, embedder=minilm_int8()),
    ),
}
