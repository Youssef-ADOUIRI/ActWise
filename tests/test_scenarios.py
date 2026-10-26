"""Checks on data/eval/risk_scenarios.csv: every gold tier must be traceable to the law."""

from collections import Counter

import pytest

from actwise.agent.schemas import TIER_ARTICLES, TIERS
from actwise.evaluation.scenarios import load_scenarios
from actwise.ids import article_id, paragraph_id
from actwise.ingest.build_chunks import load_chunks


@pytest.fixture(scope="module")
def scenarios():
    """The committed scenarios."""
    return load_scenarios()


@pytest.fixture(scope="module")
def paragraphs():
    """English paragraph id -> its text (the parts of a long paragraph joined)."""
    found: dict[str, list[str]] = {}
    for chunk in load_chunks():
        if chunk.lang == "en":
            found.setdefault(paragraph_id(chunk.id), []).append(chunk.text)
    return {pid: " ".join(parts) for pid, parts in found.items()}


def test_size_split_and_languages(scenarios):
    """40 scenarios with unique ids, 20 dev and 20 test, at least 10 in French."""
    assert len(scenarios) == 40
    assert len({s.id for s in scenarios}) == 40
    assert Counter(s.split for s in scenarios) == {"dev": 20, "test": 20}
    assert sum(s.lang == "fr" for s in scenarios) >= 10


def test_every_tier_is_in_both_splits(scenarios):
    """Each tier has clear scenarios in dev and in test."""
    for split in ("dev", "test"):
        assert {s.gold for s in scenarios if s.split == split and not s.ambiguous} == set(TIERS)


def test_evidence_is_quoted_from_the_rule(scenarios, paragraphs):
    """A rule is a paragraph of the corpus, and the evidence is quoted from it verbatim."""
    for s in scenarios:
        if s.rule:
            assert s.evidence and s.evidence in paragraphs[s.rule], s.id


def test_clear_tiers_cite_their_own_rule(scenarios):
    """Clear prohibited, high-risk and transparency scenarios rest on that tier's articles."""
    for s in scenarios:
        if not s.ambiguous and s.gold in TIER_ARTICLES:
            assert article_id(s.rule) in TIER_ARTICLES[s.gold], s.id
