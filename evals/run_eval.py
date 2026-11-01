"""Evaluate retrieval on the golden set; write evals/reports/<name>.json and .md.

    uv run --extra local python evals/run_eval.py --system hybrid --split dev
    uv run --extra local python evals/run_eval.py --system hybrid-binding --prompt answer.v1 --judge

Systems are the rows of docs/ablations.md. Questions follow the split of their
gold articles. Tune on dev; report test numbers only once, at the end of the project.
With --prompt, each question is also answered by the LLM in .env: "plain" is the step 5
baseline, answer.vN the cited pipeline. --judge scores the answers with JUDGE_MODEL.
Every LLM call is cached in .cache/llm, so a re-run costs nothing.
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
from datetime import UTC, datetime
from functools import partial
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from actwise.evaluation.answers import Ask, answer_questions, answers_markdown, plain_ask
from actwise.evaluation.generation import by_source, summarise_answers
from actwise.evaluation.golden import GOLDEN_FILE, Question, load_golden, question_split
from actwise.evaluation.judge import JUDGE_PROMPT
from actwise.evaluation.runner import SearchFn, evaluate, to_markdown
from actwise.evaluation.splits import SPLIT_FILE, load_splits, split_of
from actwise.generation.prompts import answer_prompts, load_prompt
from actwise.generation.rag import RagPipeline
from actwise.llm.factory import OFFLINE, build_judge, build_llm
from actwise.retrieval.hybrid import HybridRetriever
from actwise.retrieval.systems import SYSTEMS

REPORTS = Path("evals/reports")


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


def write_report(report: dict[str, Any], markdown: str) -> Path:
    """Write evals/reports/<name>.json and .md; returns the path without a suffix."""
    REPORTS.mkdir(parents=True, exist_ok=True)
    out = REPORTS / report["name"]  # names like answer.v1 hold a dot: add suffixes by hand
    json_text = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    Path(f"{out}.json").write_text(json_text, encoding="utf-8", newline="\n")
    Path(f"{out}.md").write_text(markdown, encoding="utf-8", newline="\n")
    return out


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
    parser.add_argument("--name", help="report name (default: <system>-<split>[-<prompt>])")
    parser.add_argument("--prompt", choices=["plain", *answer_prompts()], help="answer too")
    parser.add_argument("--judge", action="store_true", help="score the answers (with --prompt)")
    args = parser.parse_args()
    if args.judge and not args.prompt:
        parser.error("--judge needs --prompt")
    logging.basicConfig(level=logging.WARNING, format="%(message)s")
    logging.getLogger("actwise").setLevel(logging.INFO)  # our progress, not every HTTP call
    load_dotenv()  # .env fills in what the environment doesn't set
    # Built first, so a bad .env fails before any model loads.
    llm = build_llm(os.environ, OFFLINE) if args.prompt else None
    judge = build_judge(os.environ) if args.judge else None

    system = SYSTEMS[args.system]
    article_split = split_of(load_splits())
    questions = [q for q in load_golden() if question_split(q, article_split) == args.split]

    retriever = system.build()
    if isinstance(retriever, HybridRetriever) and retriever.reranker is not None:
        if llm is not None:
            parser.error("--prompt can't use a reranked system yet: both 2 GB models would load")
        search, first_ms = in_two_passes(retriever, questions)
    else:
        retriever.search("warm-up", 1)  # keep one-off start-up costs (model loading) out of timings
        search, first_ms = (lambda query, n: [hit.id for hit in retriever.search(query, n)]), 0.0

    report = {
        "name": args.name or "-".join(filter(None, [args.system, args.split, args.prompt])),
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
        ask: Ask = (
            partial(plain_ask, llm, retriever.search)
            if args.prompt == "plain"
            else RagPipeline(llm, retriever.search, load_prompt(args.prompt)).ask
        )
        rows = answer_questions(ask, questions, judge)
        cache = {"answers": [llm.hits, llm.misses], "judge": judge and [judge.hits, judge.misses]}
        answers = {
            "prompt": args.prompt,
            "judge": judge and {**judge.config, "prompt": JUDGE_PROMPT},
            "summary": summarise_answers(rows) | {"cache_hits_misses": cache},
            "by_source": by_source(rows),
            "per_question": rows,
        }
        report |= {"llm": llm.config, "answers": answers}
        markdown += answers_markdown(answers)
        s = answers["summary"]
        print(
            f"answers: refusals {s['refusal_rate']}, false refusals {s['false_refusal_rate']}, "
            f"invented {s['invented_citations']} (shown {s['invented_shown']}), "
            f"faithfulness {s['faithfulness']}, "
            f"precision strict {s['citation_precision_strict']} / lenient "
            f"{s['citation_precision_lenient']}; cache {cache}"
        )

    out = write_report(report, markdown)
    print(f"wrote {out}.json and {out}.md")


if __name__ == "__main__":
    main()
