"""Retrieval metrics at article level: gold labels are articles, not paragraphs."""

from __future__ import annotations

import math
import random
from collections.abc import Iterable

from actwise.ids import article_id


def ranked_articles(retrieved: Iterable[str]) -> list[str]:
    """Chunk ids -> article ids, duplicates removed, order kept."""
    return list(dict.fromkeys(map(article_id, retrieved)))


def recall_at_k(retrieved: list[str], gold: set[str], k: int) -> float:
    """Share of the gold articles in the top `k` distinct articles; gold must not be empty."""
    if not gold:
        raise ValueError("gold set is empty")
    top = set(ranked_articles(retrieved)[:k])
    return len(top & gold) / len(gold)


def first_hit_rank(retrieved: list[str], gold: set[str]) -> int | None:
    """1-based rank of the first gold article, or None if none was retrieved."""
    ranks = (rank for rank, a in enumerate(ranked_articles(retrieved), start=1) if a in gold)
    return next(ranks, None)


def reciprocal_rank(retrieved: list[str], gold: set[str], k: int = 10) -> float:
    """1 / rank of the first gold article in the top `k`, or 0.0 if none is there."""
    rank = first_hit_rank(retrieved, gold)
    return 1.0 / rank if rank is not None and rank <= k else 0.0


def ndcg_at_k(retrieved: list[str], gold: set[str], k: int = 10) -> float:
    """Normalised DCG with binary gains: 1.0 when the gold articles fill the top ranks."""
    ranked = ranked_articles(retrieved)[:k]
    dcg = sum(1.0 / math.log2(rank + 1) for rank, a in enumerate(ranked, start=1) if a in gold)
    ideal = sum(1.0 / math.log2(rank + 1) for rank in range(1, min(len(gold), k) + 1))
    return dcg / ideal if ideal else 0.0


def mean(values: list[float]) -> float:
    """Average of the values, or 0.0 when there are none."""
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
