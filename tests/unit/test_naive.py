from actwise.evaluation.metrics import ranked_articles
from actwise.ids import is_valid_id
from actwise.ingest.parse import Paragraph, Unit
from actwise.retrieval.naive import naive_windows


def words(prefix, n):
    return " ".join(f"{prefix}{i}" for i in range(n))


UNITS = [
    Unit("recital", "1", paragraphs=[Paragraph(None, words("r", 99))]),
    Unit("article", "5", "Prohibited AI practices", [Paragraph("1", words("a", 196))]),
]


def test_windows_ignore_structure_and_are_labelled_where_they_start():
    # Recital: "(1)" + 99 words = 100. Article: 5 heading words + 196 = 201.
    # Windows of 150 words sharing 25 start at words 0, 125 and 250.
    windows = naive_windows(UNITS, law="ai_act", lang="en", max_words=150, overlap=25)

    assert [w.id for w in windows] == ["AIA-Rec1#1", "AIA-Art5#2", "AIA-Art5#3"]
    assert "(1)" in windows[0].text and "Article 5 Prohibited AI practices" in windows[0].text
    assert all(is_valid_id(w.id) for w in windows)
    assert ranked_articles(w.id for w in windows) == ["AIA-Rec1", "AIA-Art5"]


def test_consecutive_windows_overlap():
    first, second, _ = naive_windows(UNITS, law="ai_act", lang="en", max_words=150, overlap=25)

    assert first.text.split()[-25:] == second.text.split()[:25]


def test_keys_keep_languages_apart():
    (en,) = naive_windows(UNITS[:1], law="ai_act", lang="en")
    (fr,) = naive_windows(UNITS[:1], law="ai_act", lang="fr")

    assert en.id == fr.id and en.key != fr.key
