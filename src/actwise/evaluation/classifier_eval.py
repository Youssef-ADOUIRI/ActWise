"""Run the risk classifier over scenarios and score it: accuracy, recall, confusion, downgrades."""

from __future__ import annotations

import time
from collections import Counter
from collections.abc import Callable
from typing import Any

from actwise.agent.classifier import Articles, ClassificationError, ClassifyOutcome, classify
from actwise.agent.schemas import TIERS
from actwise.evaluation.generation import share
from actwise.evaluation.metrics import mean
from actwise.evaluation.scenarios import Scenario
from actwise.generation.rag import Search
from actwise.llm.base import LLM
from actwise.llm.wrappers import CountingLLM

FAILED = "failed"  # the predicted tier of a run that hit the step budget
COSTLY = ("prohibited", "high_risk")  # the tiers where under-classifying is the costly mistake
Classifier = Callable[[LLM, Search, Articles, str], ClassifyOutcome]


def classify_scenarios(
    llm: LLM,
    search: Search,
    articles: Articles,
    scenarios: list[Scenario],
    classifier: Classifier = classify,
) -> list[dict[str, Any]]:
    """One row per scenario, with its seconds and tokens; a run over budget fails, not crashes.

    `classifier` is the agent by default, or the LangGraph version (step 10).
    """
    rows = []
    for s in scenarios:
        row: dict[str, Any] = {"id": s.id, "lang": s.lang, "ambiguous": s.ambiguous, "gold": s.gold}
        counted, start = CountingLLM(llm), time.perf_counter()
        try:
            outcome = classifier(counted, search, articles, s.description)
        except ClassificationError as exc:
            row |= {"predicted": FAILED, "error": str(exc)}
        else:
            row |= {"predicted": outcome.result.tier, "steps": outcome.steps}
            row |= {"lookups": outcome.lookups} | outcome.result.model_dump(exclude={"tier"})
        seconds = round(time.perf_counter() - start, 3)
        rows.append(
            row
            | {
                "seconds": seconds,
                "input_tokens": counted.input_tokens,
                "output_tokens": counted.output_tokens,
            }
        )
    return rows


def summarise_classifications(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Accuracy on clear and ambiguous scenarios apart, recall on the costly tiers, the downgrades.

    The 5×5 confusion matrix (gold → predicted) and the recalls count every scenario, clear
    or ambiguous. A failed run is left out of the matrix and counts as a miss in the recalls.
    Every accepted result cites only ids the agent read or retrieved: the guard in
    `agent.classifier.accept` refuses anything else, so there is nothing to measure.
    """
    clear = [r for r in rows if not r["ambiguous"]]
    ran = [r for r in rows if r["predicted"] != FAILED]
    counts = Counter((r["gold"], r["predicted"]) for r in ran)
    confusion = {gold: {tier: counts[gold, tier] for tier in TIERS} for gold in TIERS}
    return {
        "n": len(rows),
        "clear": len(clear),
        "accuracy": share([r["predicted"] == r["gold"] for r in clear]),
        "accuracy_ambiguous": share([r["predicted"] == r["gold"] for r in rows if r["ambiguous"]]),
        **{
            f"recall_{tier}": share([r["predicted"] == tier for r in rows if r["gold"] == tier])
            for tier in COSTLY
        },
        "prohibited_as_minimal": sum(
            r["gold"] == "prohibited" and r["predicted"] == "minimal_risk" for r in rows
        ),
        "dangerous_downgrades": sum(
            r["gold"] in COSTLY and r["predicted"] == "minimal_risk" for r in rows
        ),
        "failed": len(rows) - len(ran),
        "steps": round(mean([r["steps"] for r in ran]), 2),
        "lookups": round(mean([r["lookups"] for r in ran]), 2),
        "seconds": round(mean([r.get("seconds", 0) for r in rows]), 3),
        "input_tokens": round(mean([r.get("input_tokens", 0) for r in rows])),
        "confusion": confusion,
        "by_lang": {
            lang: share([r["predicted"] == r["gold"] for r in clear if r["lang"] == lang])
            for lang in sorted({r["lang"] for r in clear})
        },
    }
