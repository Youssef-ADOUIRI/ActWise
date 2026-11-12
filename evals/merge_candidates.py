"""Add the reviewed questions to the golden set: data/eval/golden.jsonl.

    uv run python evals/merge_candidates.py

Candidates marked `keep` or `fix` in data/eval/candidates.csv become q051, q052, ... in
candidate order, with `source: "synthetic"`; the hand-written questions get
`source: "hand"`. Hard questions kept in data/eval/hard_questions.csv (step 8b) follow,
under their own ids (h001, ...), with `source: "hard"`. Running it again rebuilds the
same file from the hand-written 50.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from actwise.evaluation.golden import GOLDEN_FILE, load_golden, question_split
from actwise.evaluation.splits import load_splits, split_of

CANDIDATES = Path("data/eval/candidates.csv")
HARD = Path("data/eval/hard_questions.csv")


def reviewed(path: Path) -> list[dict[str, str]]:
    """The rows of a review sheet marked `keep` or `fix`."""
    with path.open(encoding="utf-8-sig") as f:
        return [row for row in csv.DictReader(f) if row["decision"] in ("keep", "fix")]


def golden_line(row: dict[str, str], qid: str, source: str) -> dict[str, Any]:
    """One golden.jsonl line from a reviewed row."""
    line: dict[str, Any] = {
        "id": qid,
        "lang": row["lang"],
        "type": row["type"],
        "question": row["question"],
        "gold": row["gold"].split(),
        "reference": row["reference"],
    }
    if not line["gold"]:  # out of scope: the split is set by hand, not by an article
        line["split"] = row["split"]
    return line | {"source": source}


def main() -> None:
    """Rebuild golden.jsonl: the hand-written questions, every kept candidate, the hard ones."""
    article_split = split_of(load_splits())
    lines = [json.loads(line) for line in GOLDEN_FILE.read_text(encoding="utf-8").splitlines()]
    hand = [line | {"source": "hand"} for line in lines if line.get("source", "hand") == "hand"]
    kept, hard_rows = reviewed(CANDIDATES), reviewed(HARD)
    synthetic = [
        golden_line(row, f"q{n:03d}", "synthetic")
        for n, row in enumerate(kept, start=len(hand) + 1)
    ]
    hard = [golden_line(row, row["hid"], "hard") for row in hard_rows]

    text = "".join(json.dumps(line, ensure_ascii=False) + "\n" for line in hand + synthetic + hard)
    GOLDEN_FILE.write_text(text, encoding="utf-8", newline="\n")
    for question, row in zip(load_golden()[len(hand) :], kept + hard_rows, strict=True):
        assert question_split(question, article_split) == row["split"], question.id
    print(f"golden set: {len(hand)} hand-written, {len(synthetic)} synthetic, {len(hard)} hard")


if __name__ == "__main__":
    main()
