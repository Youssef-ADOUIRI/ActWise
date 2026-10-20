"""Evaluate retrieval on the golden set; write evals/reports/<name>.json and .md.

    uv run --extra local python evals/run_eval.py --system baseline --split dev

Questions follow the split of their gold articles. Tune on dev; report test
numbers only once, at the end of the project.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import subprocess
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from actwise.evaluation.golden import GOLDEN_FILE, load_golden, question_split
from actwise.evaluation.runner import evaluate, to_markdown
from actwise.evaluation.splits import SPLIT_FILE, load_splits, split_of
from actwise.retrieval.dense import DenseRetriever, Passage, build_store
from actwise.retrieval.embedders import SentenceTransformerEmbedder
from actwise.retrieval.naive import naive_passages

REPORTS = Path("evals/reports")
CACHE = Path(".cache/embeddings")
# Hub name and pinned commit. 9a0624b is the bot-made safetensors variant of main (5617a9f):
# same weights, but it loads without pickle and without transformers' silent PR redirect.
BGE_M3 = ("BAAI/bge-m3", "9a0624b896d81da7492a910ffa53731274b6cf3d")


@dataclass(frozen=True)
class System:
    description: str
    passages: Callable[[], list[Passage]]
    embedder: tuple[str, str]  # (model name, revision)


SYSTEMS = {
    "baseline": System(
        description="Baseline: fixed 150-word windows (25 shared) ignoring structure, "
        "dense BGE-M3, cosine similarity, no rerank",
        passages=naive_passages,
        embedder=BGE_M3,
    ),
}


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
    parser.add_argument("--name", help="report name (default: <system>-<split>)")
    args = parser.parse_args()
    logging.basicConfig(level=logging.WARNING, format="%(message)s")
    logging.getLogger("actwise").setLevel(logging.INFO)  # our progress, not every HTTP call

    system = SYSTEMS[args.system]
    article_split = split_of(load_splits())
    questions = [q for q in load_golden() if question_split(q, article_split) == args.split]

    passages = system.passages()
    embedder = SentenceTransformerEmbedder(*system.embedder)
    retriever = DenseRetriever(passages, embedder, build_store(passages, embedder, CACHE))
    retriever.search("warm-up", 1)  # keep one-off start-up costs out of the timings

    report = {
        "name": args.name or f"{args.system}-{args.split}",
        "created": datetime.now(UTC).isoformat(timespec="seconds"),
        "git_commit": git_commit(),
        "split": args.split,
        "system": {
            "name": args.system,
            "description": system.description,
            "embedder": embedder.config,
            "passages": len(passages),
        },
        "inputs": {"golden": fingerprint(GOLDEN_FILE), "splits": fingerprint(SPLIT_FILE)},
    } | evaluate(lambda query, n: [hit.id for hit in retriever.search(query, n)], questions)

    REPORTS.mkdir(parents=True, exist_ok=True)
    out = REPORTS / report["name"]
    json_text = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    out.with_suffix(".json").write_text(json_text, encoding="utf-8", newline="\n")
    out.with_suffix(".md").write_text(to_markdown(report), encoding="utf-8", newline="\n")

    m = report["metrics"]
    print(
        f"{report['name']}: Recall@5 {m['recall@5']:.3f}  MRR@10 {m['mrr@10']:.3f}  "
        f"nDCG@10 {m['ndcg@10']:.3f}  (n={m['n']}, {m['ms_per_query']:.0f} ms/query)"
    )
    print(f"wrote {out}.json and {out}.md")


if __name__ == "__main__":
    main()
