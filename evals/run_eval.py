"""Evaluate retrieval on the golden set; write evals/reports/<name>.json and .md.

    uv run --extra local python evals/run_eval.py --system hybrid --split dev
    uv run --extra local python evals/run_eval.py --system baseline --split dev --llm

Systems are the rows of docs/ablations.md. Questions follow the split of their
gold articles. Tune on dev; report test numbers only once, at the end of the project.
With --llm, each question is also answered from its top passages by the LLM chain
in .env (answers are cached in .cache/llm), to be scored in step 6.
"""

from __future__ import annotations

import argparse
import gc
import hashlib
import json
import logging
import os
import subprocess
import time
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Protocol

from dotenv import load_dotenv

from actwise.evaluation.answers import answer_questions, answers_markdown
from actwise.evaluation.golden import GOLDEN_FILE, Question, load_golden, question_split
from actwise.evaluation.runner import SearchFn, evaluate, to_markdown
from actwise.evaluation.splits import SPLIT_FILE, load_splits, split_of
from actwise.llm.factory import OFFLINE, build_llm
from actwise.retrieval.bm25 import BM25
from actwise.retrieval.dense import CACHE_DIR, DenseRetriever, build_store
from actwise.retrieval.embedders import BGE_M3, SentenceTransformerEmbedder
from actwise.retrieval.hybrid import HybridRetriever
from actwise.retrieval.naive import MAX_WORDS, OVERLAP, naive_passages
from actwise.retrieval.passages import Hit, Passage, chunk_passages
from actwise.retrieval.rerank import BGE_RERANKER, CrossEncoderReranker

REPORTS = Path("evals/reports")


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


def in_two_passes(hybrid: HybridRetriever, questions: list[Question]) -> tuple[SearchFn, float]:
    """Fuse for every question, free the embedder, then rerank on demand.

    The embedder and the reranker take about 2 GB each, more than this laptop can
    hold together. Rankings are exactly those of `hybrid.search()`; the returned
    float is the stage-1 time per query, which the caller adds to the rerank time.
    """
    queries = [q.question for q in questions if q.gold]
    hybrid.fused("warm-up")
    start = time.perf_counter()
    fused = {query: hybrid.fused(query) for query in queries}
    first_ms = (time.perf_counter() - start) * 1000 / len(queries)
    hybrid.dense.embedder.unload()
    gc.collect()
    hybrid.reranked("warm-up", fused[queries[0]])  # load the reranker outside the timings

    def search(query: str, n: int) -> list[str]:
        """Rerank the stage-1 list of a golden question."""
        ranked = hybrid.reranked(query, fused[query])[:n]
        return [hybrid.dense.passages[key].id for key, _ in ranked]

    return search, first_ms


def fingerprint(path: Path) -> str:
    """Short SHA-256 of a file, so a report records exactly which inputs it used."""
    return hashlib.sha256(path.read_bytes()).hexdigest()[:12]


def git_commit() -> str:
    """Short commit hash, marked "-dirty" if the working tree has uncommitted changes."""
    commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True)
    status = subprocess.run(
        ["git", "status", "--porcelain", "--", "src", "data", "evals/*.py"],
        capture_output=True,
        text=True,
    )
    return commit.stdout.strip() + ("-dirty" if status.stdout.strip() else "")


def main() -> None:
    """Evaluate one system on one split, then write the JSON and Markdown reports."""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--system", choices=SYSTEMS, default="baseline")
    parser.add_argument("--split", choices=["train", "dev", "test"], default="dev")
    parser.add_argument("--name", help="report name (default: <system>-<split>[-answers])")
    parser.add_argument(
        "--llm", action="store_true", help="also answer each question (plain prompt)"
    )
    args = parser.parse_args()
    logging.basicConfig(level=logging.WARNING, format="%(message)s")
    logging.getLogger("actwise").setLevel(logging.INFO)  # our progress, not every HTTP call
    load_dotenv()  # .env fills in what the environment doesn't set
    llm = build_llm(os.environ, OFFLINE) if args.llm else None  # a bad .env fails before any work

    system = SYSTEMS[args.system]
    article_split = split_of(load_splits())
    questions = [q for q in load_golden() if question_split(q, article_split) == args.split]

    retriever = system.build()
    if isinstance(retriever, HybridRetriever) and retriever.reranker is not None:
        if llm is not None:
            parser.error("--llm can't run a reranked system yet: both 2 GB models would be loaded")
        search, first_ms = in_two_passes(retriever, questions)
    else:
        retriever.search("warm-up", 1)  # keep one-off start-up costs (model loading) out of timings
        search, first_ms = (lambda query, n: [hit.id for hit in retriever.search(query, n)]), 0.0

    report = {
        "name": args.name or f"{args.system}-{args.split}" + ("-answers" if args.llm else ""),
        "created": datetime.now(UTC).isoformat(timespec="seconds"),
        "git_commit": git_commit(),
        "split": args.split,
        "system": {"name": args.system, "description": system.description, **retriever.config},
        "inputs": {"golden": fingerprint(GOLDEN_FILE), "splits": fingerprint(SPLIT_FILE)},
    } | evaluate(search, questions)
    if first_ms:  # timed in two passes: add the stage-1 time to the rerank time
        report["system"]["timed_in_two_passes"] = True
        report["metrics"]["ms_per_query"] = round(report["metrics"]["ms_per_query"] + first_ms, 1)

    m = report["metrics"]
    print(
        f"{report['name']}: Recall@5 {m['recall@5']:.3f}  MRR@10 {m['mrr@10']:.3f}  "
        f"nDCG@10 {m['ndcg@10']:.3f}  (n={m['n']}, {m['ms_per_query']:.0f} ms/query)"
    )

    markdown = to_markdown(report)
    if llm is not None:
        answers = answer_questions(llm, retriever.search, questions)
        answers["summary"]["cache"] = {"hits": llm.hits, "misses": llm.misses}
        report |= {"llm": llm.config, "answers": answers}
        markdown += answers_markdown(answers)
        s = answers["summary"]
        print(f"answers: {s['n']} by {s['models']}, cache {s['cache']}")

    REPORTS.mkdir(parents=True, exist_ok=True)
    out = REPORTS / report["name"]
    json_text = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    out.with_suffix(".json").write_text(json_text, encoding="utf-8", newline="\n")
    out.with_suffix(".md").write_text(markdown, encoding="utf-8", newline="\n")
    print(f"wrote {out}.json and {out}.md")


if __name__ == "__main__":
    main()
