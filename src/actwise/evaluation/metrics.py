"""Retrieval metrics at article level: gold labels are articles, not paragraphs."""

from __future__ import annotations

import math
import random
from collections.abc import Iterable

from actwise.ids import article_id


def ranked_articles(retrieved: Iterable[str]) -> list[str]:
    """Chunk ids -> article ids, duplicates removed, order kept."""
    seen: list[str] = []
    for chunk_id in retrieved:
        article = article_id(chunk_id)
        if article not in seen:
            seen.append(article)
    return seen


def recall_at_k(retrieved: list[str], gold: set[str], k: int) -> float:
    if not gold:
        raise ValueError("gold set is empty")
    top = set(ranked_articles(retrieved)[:k])
    return len(top & gold) / len(gold)


def reciprocal_rank(retrieved: list[str], gold: set[str], k: int = 10) -> float:
    for rank, article in enumerate(ranked_articles(retrieved)[:k], start=1):
        if article in gold:
            return 1.0 / rank
    return 0.0


def ndcg_at_k(retrieved: list[str], gold: set[str], k: int = 10) -> float:
    ranked = ranked_articles(retrieved)[:k]
    dcg = sum(1.0 / math.log2(rank + 1) for rank, a in enumerate(ranked, start=1) if a in gold)
    ideal = sum(1.0 / math.log2(rank + 1) for rank in range(1, min(len(gold), k) + 1))
    return dcg / ideal if ideal else 0.0


def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def bootstrap_ci(
    values: list[float], level: float = 0.95, resamples: int = 2000, seed: int = 0
) -> tuple[float, float]:
    """Confidence interval of the mean by resampling the questions with replacement.

    With 20 questions a single miss moves Recall@5 by 0.05, so every reported
    number carries this interval.
    """
    if not values:
        return 0.0, 0.0
    rng = random.Random(seed)
    means = sorted(mean(rng.choices(values, k=len(values))) for _ in range(resamples))
    low = means[int((1 - level) / 2 * resamples)]
    high = means[int((1 + level) / 2 * resamples) - 1]
    return round(low, 4), round(high, 4)
