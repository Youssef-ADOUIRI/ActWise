"""The committed training pairs (step 9): train articles only, each with its own passage."""

from actwise.evaluation.golden import NAMES_AN_ARTICLE
from actwise.evaluation.splits import load_splits
from actwise.ids import article_id
from actwise.ingest.build_chunks import load_chunks
from actwise.training.pairs import load_pairs

PAIRS = load_pairs()
SPLITS = load_splits()


def test_no_split_leakage():
    """No dev or test article is in the training pairs: it would inflate their scores."""
    articles = {article_id(p["source"].rsplit("@", 1)[0]) for p in PAIRS}

    assert not articles & (set(SPLITS["dev"]) | set(SPLITS["test"]))
    assert articles <= set(SPLITS["train"])


def test_each_pair_holds_its_source_passage_in_its_language():
    """The positive is exactly what the embedder sees for that chunk and language."""
    by_key = {c.key: c for c in load_chunks()}

    for p in PAIRS:
        assert (by_key[p["source"]].lang, by_key[p["source"]].embed_text) == (
            p["lang"],
            p["positive"],
        )


def test_no_question_names_an_article():
    """As in the golden set, a question never names its article, annex or recital."""
    assert [p["anchor"] for p in PAIRS if NAMES_AN_ARTICLE.search(p["anchor"])] == []


def test_the_pairs_are_in_the_guide_range():
    """1,000 to 1,600 pairs, and no passage is used twice."""
    assert 1000 <= len(PAIRS) <= 1600
    assert len({p["source"] for p in PAIRS}) == len(PAIRS)
