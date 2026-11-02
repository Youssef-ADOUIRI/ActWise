from actwise.generation.context import ParagraphContext
from actwise.retrieval.passages import Passage, to_hit

ART5_1 = (
    "AI Act Article 5(1): Prohibited AI practices, see paragraph 9\n"  # the header is not read
    "(h) unless strictly necessary for (iii) offences referred to in Annex II, "
    "with the safeguards of paragraph 2 and without prejudice to paragraph 1 of Article 9; "
    "deployers of points 5 (b) and (c) of Annex III"
)
PARAGRAPHS = [
    Passage("AIA-Art5-1", "en", ART5_1),
    Passage("AIA-Art5-1", "fr", "Règlement IA Article 5(1)\n(h) sauf si strictement nécessaire"),
    Passage("AIA-Art5-2", "en", "AI Act Article 5(2)\n" + "word " * 50),
    Passage("AIA-Art5-9", "en", "AI Act Article 5(9)\nA paragraph that only the header names."),
    Passage("AIA-Art9-1", "en", "AI Act Article 9(1)\nAnother article's paragraph."),
    Passage("AIA-AnnexII", "en", "AI Act Annex II\nmurder, trafficking in human beings"),
    Passage("AIA-AnnexII", "fr", "Règlement IA Annexe II\nmeurtre, traite des êtres humains"),
    Passage("AIA-AnnexIII-5", "en", "AI Act Annex III(5)\n(b) creditworthiness"),
]


def window(chunk_id, lang="en"):
    """A retrieved window of a paragraph."""
    return to_hit(Passage(chunk_id, lang, "a window"), 1.0)


def test_windows_become_whole_paragraphs_once_each():
    """Windows of one paragraph, out of order and in two languages, give it once, whole."""
    hits = [window("AIA-Art5-1#6"), window("AIA-Art5-1#5"), window("AIA-Art5-1#2", "fr")]

    chosen = ParagraphContext(PARAGRAPHS).select([*hits, window("AIA-AnnexII")], "en")

    assert [hit.key for hit in chosen] == ["AIA-Art5-1@en", "AIA-AnnexII@en"]
    assert chosen[0].text == ART5_1


def test_the_question_language_comes_first():
    """A French question reads the French copy, or the hit's language when there is none."""
    context = ParagraphContext(PARAGRAPHS)

    assert context.select([window("AIA-Art5-1#1")], "fr")[0].key == "AIA-Art5-1@fr"
    assert context.select([window("AIA-Art5-2")], "fr")[0].key == "AIA-Art5-2@en"


def test_word_budget_and_paragraph_cap():
    """A paragraph over the remaining budget is skipped; selection stops at the cap."""
    hits = [window("AIA-Art5-2"), window("AIA-AnnexII")]

    small_budget = ParagraphContext(PARAGRAPHS, word_budget=30).select(hits, "en")
    one = ParagraphContext(PARAGRAPHS, max_paragraphs=1).select(hits, "en")

    assert [hit.id for hit in small_budget] == ["AIA-AnnexII"]
    assert [hit.id for hit in one] == ["AIA-Art5-2"]


def test_references_name_annexes_and_paragraphs_of_the_same_article():
    """Annex II, point 5 of Annex III and paragraph 2; not another article's, not the header's."""
    references = ParagraphContext(PARAGRAPHS).references("AIA-Art5-1")

    assert references == ["AIA-AnnexIII-5", "AIA-AnnexII", "AIA-Art5-2"]


def test_named_units_follow_in_the_question_language_up_to_the_cap():
    """The units a chosen paragraph names are added after it, in French for a French question."""
    hits = [window("AIA-Art5-1#6", "fr")]

    plain = ParagraphContext(PARAGRAPHS).select(hits, "fr")
    followed = ParagraphContext(PARAGRAPHS, max_references=2).select(hits, "fr")

    assert [hit.key for hit in plain] == ["AIA-Art5-1@fr"]
    assert [hit.key for hit in followed] == ["AIA-Art5-1@fr", "AIA-AnnexIII-5@en", "AIA-AnnexII@fr"]
