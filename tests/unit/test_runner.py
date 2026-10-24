import pytest

from actwise.evaluation.golden import Question
from actwise.evaluation.runner import evaluate, to_markdown

QUESTIONS = [
    Question("q1", "en", "lookup", "Which practices are banned?", ("AIA-Art5",), "..."),
    Question("q2", "fr", "obligation", "Qui doit enregistrer ?", ("AIA-Art49",), "..."),
    Question("q3", "en", "not_covered", "What does the DMA say?", (), "...", split="dev"),
]

RESULTS = {
    "Which practices are banned?": ["AIA-Art5-1", "AIA-Art5-2", "AIA-Art6-1"],  # hit at rank 1
    "Qui doit enregistrer ?": ["AIA-Art71-1", "AIA-Art6-2", "AIA-Art49-1"],  # hit at rank 3
}


def search(query, n):
    """Fake retriever: canned results for each question."""
    return RESULTS[query][:n]


def test_metrics_are_averaged_over_scored_questions():
    """Metrics average the questions with gold; the out-of-scope one is skipped."""
    report = evaluate(search, QUESTIONS)

    assert report["questions"] == {"total": 3, "scored": 2, "skipped_no_gold": 1}
    assert report["metrics"]["recall@1"] == 0.5
    assert report["metrics"]["recall@5"] == 1.0
    assert report["metrics"]["mrr@10"] == pytest.approx((1 + 1 / 3) / 2, abs=1e-4)


def test_per_question_rows_show_where_the_gold_article_ranked():
    """Each row gives the rank of the first gold article and the top articles."""
    rows = {row["id"]: row for row in evaluate(search, QUESTIONS)["per_question"]}

    assert rows["q1"]["first_hit_rank"] == 1
    assert rows["q2"]["first_hit_rank"] == 3
    assert rows["q2"]["top_articles"] == ["AIA-Art71", "AIA-Art6", "AIA-Art49"]


def test_breakdowns_by_language_and_type():
    """Metrics are also reported per language and per question type."""
    report = evaluate(search, QUESTIONS)

    assert report["by_lang"]["fr"]["n"] == 1
    assert report["by_lang"]["fr"]["recall@1"] == 0.0
    assert report["by_type"]["lookup"]["mrr@10"] == 1.0
    assert report["by_source"]["hand"]["n"] == 2  # Question.source defaults to "hand"


def test_markdown_summary_lists_metrics_and_misses():
    """The Markdown report shows the main metrics and the questions missed at rank 1."""
    report = evaluate(search, QUESTIONS) | {
        "name": "toy",
        "split": "dev",
        "system": {"description": "toy retriever"},
    }

    text = to_markdown(report)

    assert "Recall@5" in text and "MRR@10" in text and "nDCG@10" in text
    assert "q2" in text  # its gold article was not first
