"""Checks on the real EUR-Lex corpus: the parser must find every official unit."""

from collections import Counter
from pathlib import Path

import pytest

from actwise.ids import is_valid_id
from actwise.ingest.build_chunks import build_chunks

RAW = Path(__file__).parents[1] / "data" / "raw"

# Official numbering of each regulation.
EXPECTED_UNITS = {
    "ai_act": {"recital": 180, "article": 113, "annex": 13},
    "gdpr": {"recital": 173, "article": 99},
}


@pytest.fixture(scope="module")
def chunks():
    """Chunks of every saved EUR-Lex page."""
    return build_chunks(RAW)


@pytest.mark.parametrize("law", EXPECTED_UNITS)
@pytest.mark.parametrize("lang", ["en", "fr"])
def test_unit_counts_match_official_numbering(chunks, law, lang):
    """The parser finds every recital, article and annex of the official numbering."""
    units = {(c.kind, c.number) for c in chunks if c.law == law and c.lang == lang}

    assert Counter(kind for kind, _ in units) == EXPECTED_UNITS[law]


def test_ids_are_valid_and_unique_per_language(chunks):
    """Every id is well formed, and no `id@lang` key appears twice."""
    assert all(is_valid_id(c.id) for c in chunks)
    keys = [c.key for c in chunks]
    assert len(keys) == len(set(keys))


@pytest.mark.parametrize("law", EXPECTED_UNITS)
def test_french_paragraphs_have_english_twins(chunks, law):
    """EN and FR give the same paragraph ids, so one gold label scores both languages."""

    def paragraph_ids(lang):
        """Paragraph ids of this law in `lang`, without the `#part` suffix."""
        return {c.id.split("#")[0] for c in chunks if c.law == law and c.lang == lang}

    assert paragraph_ids("fr") == paragraph_ids("en")


def test_total_size_is_plausible(chunks):
    """A guard against a broken parse: the chunk count stays in a plausible range."""
    assert 3000 <= len(chunks) <= 4500
