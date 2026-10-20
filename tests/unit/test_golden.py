import json

import pytest

from actwise.evaluation.golden import Question, load_golden, question_split

ARTICLE_SPLIT = {"AIA-Art5": "dev", "GDPR-Art9": "dev", "AIA-Art6": "test"}


def question(gold, split=None):
    """A question with the given gold articles and split."""
    return Question("q1", "en", "lookup", "Which practices are banned?", tuple(gold), "...", split)


def test_load_golden(tmp_path):
    """Gold lists become tuples, `split` is optional, and blank lines are skipped."""
    rows = [
        {
            "id": "q1",
            "lang": "en",
            "type": "lookup",
            "question": "Q?",
            "gold": ["AIA-Art5"],
            "reference": "R.",
        },
        {
            "id": "q2",
            "lang": "fr",
            "type": "not_covered",
            "question": "Q ?",
            "gold": [],
            "reference": "R.",
            "split": "test",
        },
    ]
    path = tmp_path / "golden.jsonl"
    path.write_text("\n".join(json.dumps(r) for r in rows) + "\n\n", encoding="utf-8")

    first, second = load_golden(path)

    assert first.gold == ("AIA-Art5",) and first.split is None
    assert second.gold == () and second.split == "test"


def test_question_takes_the_split_of_its_gold_articles():
    """A question takes the split that its gold articles share."""
    assert question_split(question(["AIA-Art5"]), ARTICLE_SPLIT) == "dev"
    assert question_split(question(["AIA-Art5", "GDPR-Art9"]), ARTICLE_SPLIT) == "dev"


def test_gold_articles_in_different_splits_are_mixed():
    """Gold articles from two splits make the question "mixed"."""
    assert question_split(question(["AIA-Art5", "AIA-Art6"]), ARTICLE_SPLIT) == "mixed"


def test_out_of_scope_question_needs_an_explicit_split():
    """A question without gold uses its own split, and must have one."""
    assert question_split(question([], split="test"), ARTICLE_SPLIT) == "test"
    with pytest.raises(ValueError):
        question_split(question([]), ARTICLE_SPLIT)
