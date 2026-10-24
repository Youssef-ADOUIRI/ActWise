"""Checks on data/eval/golden.jsonl: an evaluation is only as good as its labels."""

from collections import Counter
from pathlib import Path

import pytest

from actwise.evaluation.golden import NAMES_AN_ARTICLE, TYPES, load_golden, question_split
from actwise.evaluation.splits import load_splits, split_of
from actwise.ids import article_id

EVAL = Path(__file__).parents[1] / "data" / "eval"


@pytest.fixture(scope="module")
def questions():
    """The committed golden set."""
    return load_golden(EVAL / "golden.jsonl")


@pytest.fixture(scope="module")
def article_split():
    """Article id -> split, from the committed splits."""
    return split_of(load_splits(EVAL / "splits.json"))


def test_size_and_languages(questions):
    """At least 150 questions with unique ids, in both languages, 15+ in French."""
    langs = Counter(q.lang for q in questions)

    assert len(questions) >= 150
    assert len({q.id for q in questions}) == len(questions)
    assert set(langs) == {"en", "fr"}
    assert langs["fr"] >= 15


def test_every_question_type_is_used(questions):
    """Every type in `TYPES` appears at least once."""
    assert {q.type for q in questions} == set(TYPES)


def test_gold_labels_are_articles_of_the_corpus(questions, article_split):
    """Gold labels are article-level ids found in the corpus: a typo would zero a question."""
    for q in questions:
        for gold in q.gold:
            assert article_id(gold) == gold, f"{q.id}: {gold} is not article-level"
            assert gold in article_split, f"{q.id}: {gold} is not in the corpus"


def test_only_out_of_scope_questions_have_no_gold(questions):
    """Only `not_covered` questions lack gold, and they carry a dev or test split."""
    for q in questions:
        if q.type == "not_covered":
            assert not q.gold and q.split in ("dev", "test"), q.id
        else:
            assert q.gold and q.split is None, q.id


def test_cross_law_questions_cite_both_laws(questions):
    """A cross-law question has gold articles in both the AI Act and the GDPR."""
    for q in questions:
        if q.type == "cross_law":
            assert {gold.split("-")[0] for gold in q.gold} == {"AIA", "GDPR"}, q.id


def test_no_question_spans_two_splits(questions, article_split):
    """The gold articles of each question sit in one split; otherwise it fits none."""
    mixed = [q.id for q in questions if question_split(q, article_split) == "mixed"]

    assert not mixed


def test_dev_and_test_have_enough_scored_questions(questions, article_split):
    """Dev and test each have at least 50 scored and 10 out-of-scope questions (decision 002)."""
    scored = Counter(question_split(q, article_split) for q in questions if q.gold)
    refusals = Counter(q.split for q in questions if not q.gold)

    assert scored["dev"] >= 50 and scored["test"] >= 50
    assert refusals["dev"] >= 10 and refusals["test"] >= 10


def test_sources(questions):
    """Every question is hand-written or reviewed synthetic; the 50 hand-written ones come first."""
    assert {q.source for q in questions} == {"hand", "synthetic"}
    assert [q.source for q in questions[:50]] == ["hand"] * 50
    assert all(q.source == "synthetic" for q in questions[50:])


def test_questions_do_not_name_the_article(questions):
    """No question names an article, annex or recital by its number."""
    assert not [q.id for q in questions if NAMES_AN_ARTICLE.search(q.question)]
