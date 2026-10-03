"""Build data/processed/chunks.jsonl from the saved EUR-Lex pages.

Run from the repo root: `make ingest`
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from actwise.ingest.chunk import Chunk, chunk_units
from actwise.ingest.html import html_to_text
from actwise.ingest.parse import parse_regulation

SOURCES = [("ai_act", "en"), ("ai_act", "fr"), ("gdpr", "en"), ("gdpr", "fr")]
RAW_DIR = Path("data/raw")
OUT_FILE = Path("data/processed/chunks.jsonl")


def build_chunks(raw_dir: Path = RAW_DIR) -> list[Chunk]:
    chunks: list[Chunk] = []
    for law, lang in SOURCES:
        units = parse_regulation(html_to_text(raw_dir / f"{law}.{lang}.html"))
        chunks += chunk_units(units, law, lang)
    return chunks


def write_jsonl(chunks: list[Chunk], path: Path = OUT_FILE) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as f:
        for chunk in chunks:
            f.write(json.dumps(chunk.to_json(), ensure_ascii=False) + "\n")


def summary(chunks: list[Chunk]) -> str:
    """One line per source: units of each kind and number of chunks."""
    lines = []
    for law, lang in SOURCES:
        mine = [c for c in chunks if c.law == law and c.lang == lang]
        units = Counter(kind for kind, _ in {(c.kind, c.number) for c in mine})
        lines.append(
            f"{law:6} {lang}  recitals={units['recital']:3}  articles={units['article']:3}  "
            f"annexes={units['annex']:2}  chunks={len(mine)}"
        )
    lines.append(f"total chunks={len(chunks)}")
    return "\n".join(lines)


def main() -> None:
    chunks = build_chunks()
    write_jsonl(chunks)
    print(summary(chunks))
    print(f"wrote {OUT_FILE}")


if __name__ == "__main__":
    main()
