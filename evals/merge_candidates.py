"""Add the reviewed candidates to the golden set: data/eval/golden.jsonl.

    uv run python evals/merge_candidates.py

Candidates marked `keep` or `fix` in data/eval/candidates.csv become q051, q052, ... in
candidate order, with `source: "synthetic"`; the hand-written questions get
`source: "hand"`. Running it again rebuilds the same file from the hand-written 50.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

from actwise.evaluation.golden import GOLDEN_FILE, load_golden, question_split
from actwise.evaluation.splits import load_splits, split_of

CANDIDATES = Path("data/eval/candidates.csv")


def main() -> None:
    """Rebuild golden.jsonl: the hand-written questions, then every kept candidate."""
    article_split = split_of(load_splits())
    lines = [json.loads(line) for line in GOLDEN_FILE.read_text(encoding="utf-8").splitlines()]
    hand = [line | {"source": "hand"} for line in lines if line.get("source", "hand") == "hand"]
    with CANDIDATES.open(encoding="utf-8-sig") as f:
        kept = [row for row in csv.DictReader(f) if row["decision"] in ("keep", "fix")]

    synthetic = []
    for n, row in enumerate(kept, start=len(hand) + 1):
        line = {
            "id": f"q{n:03d}",
            "lang": row["lang"],
            "type": row["type"],
            "question": row["question"],
            "gold": row["gold"].split(),
            "reference": row["reference"],
        }
        if not line["gold"]:  # out of scope: the split is set by hand, not by an article
            line["split"] = row["split"]
        synthetic.append(line | {"source": "synthetic"})

    text = "".join(json.dumps(line, ensure_ascii=False) + "\n" for line in hand + synthetic)
    GOLDEN_FILE.write_text(text, encoding="utf-8", newline="\n")
    for question, row in zip(load_golden()[len(hand) :], kept, strict=True):
        assert question_split(question, article_split) == row["split"], question.id
    print(f"golden set: {len(hand)} hand-written + {len(synthetic)} synthetic questions")


if __name__ == "__main__":
    main()
