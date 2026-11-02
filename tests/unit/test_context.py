from actwise.generation.context import ParagraphContext
from actwise.retrieval.passages import Passage, to_hit

PARAGRAPHS = [
    Passage(
        "AIA-Art5-1", "en", "AI Act Article 5(1)\n(h) unless strictly necessary for: (i) ... (iii)"
    ),
    Passage("AIA-Art5-1", "fr", "Règlement IA Article 5(1)\n(h) sauf si strictement nécessaire"),
    Passage("AIA-Art5-2", "en", "AI Act Article 5(2)\n" + "word " * 50),
    Passage("AIA-AnnexII", "en", "AI Act Annex II\nmurder, trafficking in human beings"),
]


def window(chunk_id, lang="en"):
    """A retrieved window of a paragraph."""
    return to_hit(Passage(chunk_id, lang, "a window"), 1.0)


def test_windows_become_whole_paragraphs_once_each():
    """Windows of one paragraph, out of order and in two languages, give it once, whole."""
    hits = [window("AIA-Art5-1#6"), window("AIA-Art5-1#5"), window("AIA-Art5-1#2", "fr")]

    chosen = ParagraphContext(PARAGRAPHS).select([*hits, window("AIA-AnnexII")], "en")

    assert [hit.key for hit in chosen] == ["AIA-Art5-1@en", "AIA-AnnexII@en"]
    assert chosen[0].text == PARAGRAPHS[0].text


def test_the_question_language_comes_first():
    """A French question reads the French copy, or the hit's language when there is none."""
    context = ParagraphContext(PARAGRAPHS)

    assert context.select([window("AIA-Art5-1#1")], "fr")[0].key == "AIA-Art5-1@fr"
    assert context.select([window("AIA-AnnexII")], "fr")[0].key == "AIA-AnnexII@en"


def test_word_budget_and_paragraph_cap():
    """A paragraph over the remaining budget is skipped; selection stops at the cap."""
    hits = [window("AIA-Art5-2"), window("AIA-AnnexII")]

    small_budget = ParagraphContext(PARAGRAPHS, word_budget=30).select(hits, "en")
    one = ParagraphContext(PARAGRAPHS, max_paragraphs=1).select(hits, "en")

    assert [hit.id for hit in small_budget] == ["AIA-AnnexII"]
    assert [hit.id for hit in one] == ["AIA-Art5-2"]
