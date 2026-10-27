"""Run the risk classifier over scenarios and score it: accuracy, confusion, downgrades."""

from __future__ import annotations

from collections import Counter
from typing import Any

from actwise.agent.classifier import Articles, ClassificationError, classify
from actwise.agent.schemas import TIERS
from actwise.evaluation.generation import share
from actwise.evaluation.metrics import mean
from actwise.evaluation.scenarios import Scenario
from actwise.generation.rag import Search
from actwise.llm.base import LLM

FAILED = "failed"  # the predicted tier of a run that hit the step budget


def classify_scenarios(
    llm: LLM, search: Search, articles: Articles, scenarios: list[Scenario]
) -> list[dict[str, Any]]:
    """One row per scenario; a run that exhausts the step budget is a failure, not a crash."""
    rows = []
    for s in scenarios:
        row: dict[str, Any] = {"id": s.id, "lang": s.lang, "ambiguous": s.ambiguous, "gold": s.gold}
        try:
            outcome = classify(llm, search, articles, s.description)
        except ClassificationError as exc:
            row |= {"predicted": FAILED, "error": str(exc)}
        else:
            row |= {"predicted": outcome.result.tier, "steps": outcome.steps}
            row |= {"lookups": outcome.lookups} | outcome.result.model_dump(exclude={"tier"})
        rows.append(row)
    return rows


def summarise_classifications(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Accuracy on clear and ambiguous scenarios apart, the confusion matrix and the downgrades.

    Every accepted result cites only ids the agent read or retrieved: the guard in
    `agent.classifier.accept` refuses anything else, so there is nothing to measure.
    """
    clear = [r for r in rows if not r["ambiguous"]]
    ran = [r for r in rows if r["predicted"] != FAILED]
    confusion = {
        gold: dict(Counter(r["predicted"] for r in clear if r["gold"] == gold))
        for gold in TIERS
        if any(r["gold"] == gold for r in clear)
    }
    return {
        "n": len(rows),
        "clear": len(clear),
        "accuracy": share([r["predicted"] == r["gold"] for r in clear]),
        "accuracy_ambiguous": share([r["predicted"] == r["gold"] for r in rows if r["ambiguous"]]),
        "prohibited_as_minimal": sum(
            r["gold"] == "prohibited" and r["predicted"] == "minimal_risk" for r in rows
        ),
        "dangerous_downgrades": sum(
            r["gold"] in ("prohibited", "high_risk") and r["predicted"] == "minimal_risk"
            for r in rows
        ),
        "failed": len(rows) - len(ran),
        "steps": round(mean([r["steps"] for r in ran]), 2),
        "lookups": round(mean([r["lookups"] for r in ran]), 2),
        "confusion": confusion,
        "by_lang": {
            lang: share([r["predicted"] == r["gold"] for r in clear if r["lang"] == lang])
            for lang in sorted({r["lang"] for r in clear})
        },
    }
