"""The naive baseline: fixed windows over the whole text, ignoring its structure.

Windows run across article boundaries on purpose; that is what "naive" means.
Each window is labelled with the article where it starts (`AIA-Art5#12` is the
12th window, starting in Article 5), so the article-level metrics still apply.
"""

from __future__ import annotations

from pathlib import Path

from actwise.ingest.build_chunks import RAW_DIR, SOURCES, parse_source
from actwise.ingest.chunk import unit_id, window_starts
from actwise.ingest.parse import Unit
from actwise.retrieval.passages import Passage

MAX_WORDS, OVERLAP = 150, 25  # the baseline's windows; independent of chunk.py's defaults
HEADING = {
    "en": {"article": "Article", "annex": "ANNEX"},
    "fr": {"article": "Article", "annex": "ANNEXE"},
}


def unit_text(unit: Unit, lang: str) -> str:
    """The unit as it reads in the regulation: heading, then its paragraphs."""
    if unit.kind == "recital":
        heading = f"({unit.number})"
    else:
        heading = f"{HEADING[lang][unit.kind]} {unit.number} {unit.title}"
    return " ".join([heading, *(p.text for p in unit.paragraphs)])


def naive_windows(
    units: list[Unit], law: str, lang: str, max_words: int = MAX_WORDS, overlap: int = OVERLAP
) -> list[Passage]:
    """Fixed windows over the units laid end to end, each labelled with the article it starts in."""
    words: list[str] = []
    owners: list[str] = []  # article id of each word
    for unit in units:
        unit_words = unit_text(unit, lang).split()
        words += unit_words
        owners += [unit_id(unit, law)] * len(unit_words)

    starts = window_starts(len(words), max_words, overlap)
    return [
        Passage(f"{owners[start]}#{n}", lang, " ".join(words[start : start + max_words]))
        for n, start in enumerate(starts, start=1)
    ]


def naive_passages(raw_dir: Path = RAW_DIR) -> list[Passage]:
    """Baseline passages for every page in `SOURCES`."""
    passages: list[Passage] = []
    for law, lang in SOURCES:
        passages += naive_windows(parse_source(law, lang, raw_dir), law, lang)
    return passages
