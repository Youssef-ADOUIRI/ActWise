"""Draft the embedder's training pairs: data/train/pairs.jsonl and a review sheet.

    uv run python evals/make_pairs.py      (make pairs)

About 800 train article and annex paragraphs each get a question in English and in
French from the offline chain (cached, so a re-run makes no API call). Rules drop the
obvious failures. 50 kept pairs go to pairs_review.csv: a reviewer marks each one keep
or drop, and a re-run leaves the dropped ones out of pairs.jsonl. An existing review
sheet is never overwritten, so its decisions survive a re-run.
"""

from __future__ import annotations

import csv
import json
import os
from collections import Counter
from pathlib import Path

from dotenv import load_dotenv

from actwise.evaluation.splits import load_splits, split_of
from actwise.ingest.build_chunks import load_chunks
from actwise.llm.factory import OFFLINE, build_llm
from actwise.training.pairs import PAIRS_FILE, make_pairs, review_sample

N_CHUNKS, REVIEW_SIZE = 800, 50
REVIEW_FILE = Path("data/train/pairs_review.csv")
COLUMNS = ["source", "lang", "anchor", "positive", "decision", "note"]


def read_drops(path: Path) -> set[str]:
    """Sources of the pairs a reviewer marked drop; none before the sheet exists."""
    if not path.exists():
        return set()
    with path.open(encoding="utf-8-sig", newline="") as f:
        return {row["source"] for row in csv.DictReader(f) if row["decision"] == "drop"}


def main() -> None:
    """Draft and screen every pair, write the review sheet once, then the kept pairs."""
    load_dotenv()
    pairs = make_pairs(
        build_llm(os.environ, OFFLINE), load_chunks(), split_of(load_splits()), N_CHUNKS
    )
    kept = [p for p in pairs if not p["screen"]]
    if not REVIEW_FILE.exists():
        with REVIEW_FILE.open("w", encoding="utf-8-sig", newline="") as f:  # BOM: Excel reads é
            writer = csv.DictWriter(f, COLUMNS, extrasaction="ignore", lineterminator="\n")
            writer.writeheader()
            writer.writerows(review_sample(kept, REVIEW_SIZE))
    drops = read_drops(REVIEW_FILE)
    final = [p for p in kept if p["source"] not in drops]
    fields = ("source", "lang", "anchor", "positive")
    with PAIRS_FILE.open("w", encoding="utf-8", newline="\n") as f:
        f.writelines(
            json.dumps({k: p[k] for k in fields}, ensure_ascii=False) + "\n" for p in final
        )

    reasons = Counter(r for p in pairs for r in p["screen"].split("; ") if r)
    print(f"drafted {len(pairs)} pairs; dropped by rule: {dict(reasons) or 'none'}")
    print(f"dropped in review: {len(drops)}; wrote {len(final)} to {PAIRS_FILE}")
    print(f"by language: {dict(Counter(p['lang'] for p in final))}")


if __name__ == "__main__":
    main()
