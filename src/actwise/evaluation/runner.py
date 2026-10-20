"""Run a retriever over golden questions and score it at article level."""

from __future__ import annotations

import time
from collections import defaultdict
from collections.abc import Callable
from typing import Any

from actwise.evaluation.golden import Question
from actwise.evaluation.metrics import (
    bootstrap_ci,
    first_hit_rank,
    mean,
    ndcg_at_k,
    ranked_articles,
    recall_at_k,
    reciprocal_rank,
)

SearchFn = Callable[[str, int], list[str]]  # (query, n) -> chunk ids, best first
RECALL_AT = (1, 5, 10, 20)
METRICS = [*(f"recall@{k}" for k in RECALL_AT), "mrr@10", "ndcg@10"]
POOL = 50  # passages fetched per query; the metrics deduplicate them to articles


def score_question(question: Question, retrieved: list[str]) -> dict[str, Any]:
    """One report row: rank of the first gold article, the top articles and every metric."""
    gold = set(question.gold)
    return {
        "id": question.id,
        "lang": question.lang,
        "type": question.type,
        "gold": list(question.gold),
        "first_hit_rank": first_hit_rank(retrieved, gold),
        "top_articles": ranked_articles(retrieved)[:10],
        **{f"recall@{k}": recall_at_k(retrieved, gold, k) for k in RECALL_AT},
        "mrr@10": reciprocal_rank(retrieved, gold, 10),
        "ndcg@10": ndcg_at_k(retrieved, gold, 10),
    }


def summarise(rows: list[dict[str, Any]]) -> dict[str, float]:
    """Rounded mean of each metric over the rows, plus their count `n`."""
    return {"n": len(rows), **{m: round(mean([r[m] for r in rows]), 4) for m in METRICS}}


def breakdown(rows: list[dict[str, Any]], field: str) -> dict[str, dict[str, float]]:
    """`summarise()` for each value of `field`, such as each language or question type."""
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[row[field]].append(row)
    return {name: summarise(group) for name, group in sorted(groups.items())}


def evaluate(search: SearchFn, questions: list[Question]) -> dict[str, Any]:
    """Score every question that has gold articles.

    Out-of-scope questions (no gold) have nothing to retrieve; they are scored
    on refusals once the answer generator exists (step 6).
    """
    rows, timings = [], []
    for question in questions:
        if not question.gold:
            continue
        start = time.perf_counter()
        retrieved = search(question.question, POOL)
        timings.append((time.perf_counter() - start) * 1000)
        rows.append(score_question(question, retrieved))

    return {
        "questions": {
            "total": len(questions),
            "scored": len(rows),
            "skipped_no_gold": len(questions) - len(rows),
        },
        "metrics": summarise(rows) | {"ms_per_query": round(mean(timings), 1)},
        "ci95": {m: bootstrap_ci([r[m] for r in rows]) for m in ("recall@5", "mrr@10")},
        "by_lang": breakdown(rows, "lang"),
        "by_type": breakdown(rows, "type"),
        "per_question": rows,
    }


def interval(bounds: tuple[float, float]) -> str:
    """(0.45, 0.85) -> '[0.45, 0.85]'."""
    return f"[{bounds[0]:.2f}, {bounds[1]:.2f}]"


def to_markdown(report: dict[str, Any]) -> str:
    """Render a report as Markdown: metrics, breakdowns, and the questions missed at rank 1."""
    m, ci = report["metrics"], report["ci95"]
    lines = [
        f"# Retrieval report: {report['name']}",
        "",
        f"{report['system']['description']}. Split `{report['split']}`, "
        f"{m['n']} scored questions ({report['questions']['skipped_no_gold']} out-of-scope "
        "questions skipped). Metrics are at article level; 95 % bootstrap intervals in brackets.",
        "",
        "| Metric | Value |",
        "|---|---|",
        f"| Recall@1 | {m['recall@1']:.3f} |",
        f"| **Recall@5** | **{m['recall@5']:.3f}** {interval(ci['recall@5'])} |",
        f"| Recall@10 | {m['recall@10']:.3f} |",
        f"| Recall@20 | {m['recall@20']:.3f} |",
        f"| MRR@10 | {m['mrr@10']:.3f} {interval(ci['mrr@10'])} |",
        f"| nDCG@10 | {m['ndcg@10']:.3f} |",
        f"| ms / query | {m['ms_per_query']:.0f} |",
    ]
    for title, field in (("By language", "by_lang"), ("By question type", "by_type")):
        lines += ["", f"## {title}", "", "| | n | Recall@5 | MRR@10 |", "|---|---|---|---|"]
        lines += [
            f"| {name} | {g['n']} | {g['recall@5']:.3f} | {g['mrr@10']:.3f} |"
            for name, g in report[field].items()
        ]

    misses = [r for r in report["per_question"] if r["first_hit_rank"] != 1]
    misses.sort(key=lambda r: (r["first_hit_rank"] is None, r["first_hit_rank"] or 0))
    lines += [
        "",
        "## Questions whose gold article is not ranked first",
        "",
        "| Question | Gold | First hit | Top 3 retrieved |",
        "|---|---|---|---|",
    ]
    lines += [
        f"| {r['id']} ({r['lang']}) | {', '.join(r['gold'])} | {r['first_hit_rank'] or 'none'} "
        f"| {', '.join(r['top_articles'][:3])} |"
        for r in misses
    ]
    return "\n".join(lines) + "\n"
