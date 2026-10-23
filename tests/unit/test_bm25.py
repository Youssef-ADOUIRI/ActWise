from actwise.retrieval.bm25 import BM25, tokenize
from actwise.retrieval.passages import Passage

PASSAGES = [
    Passage(
        "GDPR-Art17-1",
        "en",
        "Right to erasure. The data subject shall have the right to obtain from the "
        "controller the erasure of personal data concerning him or her.",
    ),
    Passage(
        "AIA-Art5-1",
        "en",
        "Prohibited AI practices: AI systems for the social scoring of natural persons.",
    ),
    Passage(
        "AIA-Art9-1",
        "en",
        "A risk management system shall be established for high-risk AI systems.",
    ),
    Passage(
        "GDPR-Art17-1",
        "fr",
        "Droit à l’effacement. La personne concernée a le droit d’obtenir du responsable "
        "du traitement l’effacement de données à caractère personnel la concernant.",
    ),
]


def test_tokenize_folds_accents_and_splits_elisions():
    """Accents are folded and French elisions split, so plain-keyboard queries match."""
    assert tokenize("L’accès aux Données") == ["l", "acces", "aux", "donnees"]


def test_bm25():
    """An exact term ranks its article first; unknown words return nothing."""
    bm25 = BM25(PASSAGES)

    assert bm25.search("right to erasure")[0].key == "GDPR-Art17-1@en"
    assert bm25.search("social scoring")[0].key == "AIA-Art5-1@en"
    assert bm25.search("quantum blockchain") == []


def test_french_query_without_accents_finds_the_french_text():
    """A query typed without accents still matches the accented French passage."""
    hits = BM25(PASSAGES).search("droit a l'effacement des donnees", top_k=2)

    assert hits[0].key == "GDPR-Art17-1@fr"
    assert hits[0].score > hits[1].score
