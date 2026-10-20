"""Split the corpus by article into train / dev / test, before any question is written.

Splitting by article, not by chunk, keeps the paragraphs of one article in the
same split. Random chunks would leak neighbouring text into the test set.
Train articles are kept for fine-tuning pairs (step 9), dev for tuning, test
for the reported numbers.

Run from the repo root: `make splits`
"""

from __future__ import annotations

import json
import random
from collections import Counter
from collections.abc import Iterable
from pathlib import Path

from actwise.ids import article_id, parse_id

CHUNK_FILE = Path("data/processed/chunks.jsonl")
SPLIT_FILE = Path("data/eval/splits.json")
SEED = 42


def make_splits(article_ids: Iterable[str], seed: int = SEED) -> dict[str, list[str]]:
    """70 % train, 15 % dev, 15 % test, by a seeded shuffle of the sorted ids."""
    ids = sorted(set(article_ids))
    random.Random(seed).shuffle(ids)
    train_end, dev_end = int(0.70 * len(ids)), int(0.85 * len(ids))
    return {
        "train": sorted(ids[:train_end]),
        "dev": sorted(ids[train_end:dev_end]),
        "test": sorted(ids[dev_end:]),
    }


def split_of(splits: dict[str, list[str]]) -> dict[str, str]:
    """Article id -> split name."""
    return {article: name for name, articles in splits.items() for article in articles}


def load_splits(path: Path = SPLIT_FILE) -> dict[str, list[str]]:
    """Read the committed splits: split name -> sorted article ids."""
    return json.loads(path.read_text(encoding="utf-8"))


def corpus_articles(chunk_file: Path = CHUNK_FILE) -> list[str]:
    """Every article-level id in the chunk file, recitals and annexes included, sorted."""
    with chunk_file.open(encoding="utf-8") as f:
        return sorted({article_id(json.loads(line)["id"]) for line in f})


def main() -> None:
    """Write `SPLIT_FILE` and print each split's counts by kind."""
    splits = make_splits(corpus_articles())
    SPLIT_FILE.parent.mkdir(parents=True, exist_ok=True)
    SPLIT_FILE.write_text(json.dumps(splits, indent=2) + "\n", encoding="utf-8", newline="\n")
    for name, articles in splits.items():
        kinds = Counter((parse_id(a) or {}).get("tag") for a in articles)
        print(f"{name:5} {len(articles):3} units  {dict(kinds)}")
    print(f"wrote {SPLIT_FILE}")


if __name__ == "__main__":
    main()
