"""The golden set: hand-written questions with article-level gold labels.

One JSON object per line in data/eval/golden.jsonl:

    {"id": "q001", "lang": "en", "type": "lookup", "question": "...",
     "gold": ["AIA-Art5"], "reference": "..."}

A question belongs to the split of its gold articles. Out-of-scope questions
have no gold article ("gold": []), so they carry an explicit "split" instead.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

GOLDEN_FILE = Path("data/eval/golden.jsonl")
TYPES = ("lookup", "definition", "obligation", "cross_law", "not_covered")


@dataclass(frozen=True)
class Question:
    id: str
    lang: str  # "en" | "fr"
    type: str  # one of TYPES
    question: str
    gold: tuple[str, ...]  # article-level ids, such as "AIA-Art5"; empty if out of scope
    reference: str  # one-sentence reference answer, used for generation metrics later
    split: str | None = None  # only for out-of-scope questions


def load_golden(path: Path = GOLDEN_FILE) -> list[Question]:
    questions = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            row = json.loads(line)
            questions.append(Question(**{**row, "gold": tuple(row["gold"])}))
    return questions


def question_split(question: Question, article_split: dict[str, str]) -> str:
    """The split of the question's gold articles, or "mixed" if they disagree."""
    if not question.gold:
        if question.split is None:
            raise ValueError(f"{question.id}: an out-of-scope question needs a 'split'")
        return question.split
    splits = {article_split[article] for article in question.gold}
    return splits.pop() if len(splits) == 1 else "mixed"
