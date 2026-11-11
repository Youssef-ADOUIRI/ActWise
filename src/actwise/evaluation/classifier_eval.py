"""Run the risk classifier over scenarios and score it: accuracy, confusion, downgrades."""

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
from actwise.llm.base import LLM, LLMResponse

FAILED = "failed"  # the predicted tier of a run that hit the step budget
Classifier = Callable[[LLM, Search, Articles, str], ClassifyOutcome]


class TokenCount:
    """An LLM that adds up the tokens of every reply, cached ones included."""

    def __init__(self, llm: LLM):
        """Wrap `llm`; nothing counted yet."""
        self.llm, self.config = llm, llm.config
        self.input = self.output = 0

    def chat(self, *args: Any, **kwargs: Any) -> LLMResponse:
        """Ask the wrapped model and count what the reply cost."""
        reply = self.llm.chat(*args, **kwargs)
        self.input += reply.input_tokens
        self.output += reply.output_tokens
        return reply


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
        counted, start = TokenCount(llm), time.perf_counter()
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
            | {"seconds": seconds, "input_tokens": counted.input, "output_tokens": counted.output}
        )
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
        "seconds": round(mean([r.get("seconds", 0) for r in rows]), 3),
        "input_tokens": round(mean([r.get("input_tokens", 0) for r in rows])),
        "confusion": confusion,
        "by_lang": {
            lang: share([r["predicted"] == r["gold"] for r in clear if r["lang"] == lang])
            for lang in sorted({r["lang"] for r in clear})
        },
    }
