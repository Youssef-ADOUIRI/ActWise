"""Scores for a set of answers: refusals, citations, gold articles in context, faithfulness.

Each row is one answered question (see `evaluation/answers.py`); rows with a `judge`
verdict also get faithfulness and lenient citation precision.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Sequence
from typing import Any

from actwise.evaluation.metrics import bootstrap_ci, mean
from actwise.generation.citations import extract_citations, uncited_sentences
from actwise.ids import article_id


def share(values: Sequence[float]) -> float | None:
    """The mean rounded to 4 places (a rate, for booleans), or None when there is nothing."""
    return round(sum(values) / len(values), 4) if values else None


def summarise_answers(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """The headline numbers of `docs/generation.md` for one set of answers."""
    in_scope = [r for r in rows if r["gold"]]
    out_of_scope = [r for r in rows if not r["gold"]]
    answered = [r for r in rows if not r["refused"]]
    judged = [r for r in answered if (r.get("judge") or {}).get("score") is not None]
    strict = [article_id(c) in r["gold"] for r in in_scope for c in r["citations"]]
    gold_in_context = [
        any(article_id(s["id"]) in r["gold"] for s in r["sources"]) for r in in_scope
    ]
    gold_cited = [any(article_id(c) in r["gold"] for c in r["citations"]) for r in in_scope]
    lenient = [c not in r["judge"]["unsupported"] for r in judged for c in r["citations"]]
    faithfulness = [(r["judge"]["score"] - 1) / 4 for r in judged]
    return {
        "n": len(rows),
        "in_scope": len(in_scope),
        "out_of_scope": len(out_of_scope),
        "refusal_rate": share([r["refused"] for r in out_of_scope]),
        "false_refusal_rate": share([r["refused"] for r in in_scope]),
        "refusal_reasons": dict(Counter(r["reason"] for r in rows if r["refused"])),
        "retried": sum(1 for r in rows if r.get("retried")),  # refused once, rewritten (step 8b)
        "invented_citations": sum(len(r["invented"]) for r in rows),
        "invented_shown": sum(
            1 for r in rows for c in r["invented"] if c in extract_citations(r["answer"])
        ),
        "citation_precision_strict": share(strict),
        # per in-scope question: did the model read a gold article, and did it cite one?
        "gold_in_context": share(gold_in_context),
        "gold_cited": share(gold_cited),
        "citation_precision_lenient": share(lenient),
        "faithfulness": share(faithfulness),
        # score 5: no unsupported claim at all, where judge and humans agree best (kappa 0.95)
        "fully_supported": share([r["judge"]["score"] == 5 for r in judged]),
        "faithfulness_ci95": bootstrap_ci(faithfulness) if faithfulness else None,
        "judged": len(judged),
        "judge_failed": sum(1 for r in answered if "judge" in r and r["judge"]["score"] is None),
        "uncited_sentences": round(mean([uncited_sentences(r["answer"]) for r in answered]), 2),
        "models": dict(Counter(r["model"] for r in rows if r["model"])),
        "input_tokens": sum(r["input_tokens"] for r in rows),
        "output_tokens": sum(r["output_tokens"] for r in rows),
    }


def by_source(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """`summarise_answers()` for the hand-written and the synthetic questions apart."""
    return {
        source: summarise_answers([r for r in rows if r["source"] == source])
        for source in sorted({r["source"] for r in rows})
    }
