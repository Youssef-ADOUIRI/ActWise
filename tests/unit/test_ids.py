import pytest

from actwise.ids import article_id, human_label, is_valid_id


@pytest.mark.parametrize(
    "chunk_id",
    [
        "AIA-Art6-2",
        "AIA-AnnexIII-4",
        "GDPR-Art17",
        "AIA-Rec63",
        "AIA-Art3-12#2",
        "AIA-Art3-0",
        "AIA-AnnexVIII-b.1",
    ],
)
def test_valid_ids(chunk_id):
    assert is_valid_id(chunk_id)


@pytest.mark.parametrize(
    "chunk_id", ["", "1", "note", "AIA", "aia-Art6", "AIA-Article6", "AIA-Art6-", "AIA-Art6-2."]
)
def test_invalid_ids(chunk_id):
    assert not is_valid_id(chunk_id)


def test_article_id_drops_paragraph_and_part():
    assert article_id("AIA-Art6-2#1") == "AIA-Art6"
    assert article_id("AIA-AnnexIII-4") == "AIA-AnnexIII"
    assert article_id("GDPR-Rec10") == "GDPR-Rec10"


def test_article_id_rejects_garbage():
    with pytest.raises(ValueError):
        article_id("not an id")


@pytest.mark.parametrize(
    ("chunk_id", "lang", "label"),
    [
        ("AIA-Art6-2", "en", "AI Act, Art. 6(2)"),
        ("AIA-Art3-0", "en", "AI Act, Art. 3"),
        ("GDPR-Art17", "fr", "RGPD, Art. 17"),
        ("AIA-AnnexIII-4", "en", "AI Act, Annex III, point 4"),
        ("AIA-AnnexIII-4", "fr", "Règlement IA, Annexe III, point 4"),
        ("AIA-AnnexVIII-b.1", "en", "AI Act, Annex VIII, Section B, point 1"),
        ("AIA-AnnexVIII-a.0", "en", "AI Act, Annex VIII, Section A"),
        ("AIA-AnnexXI-2.1", "fr", "Règlement IA, Annexe XI, Section 2, point 1"),
        ("AIA-Rec63", "fr", "Règlement IA, considérant 63"),
        ("garbage", "en", "garbage"),
    ],
)
def test_human_label(chunk_id, lang, label):
    assert human_label(chunk_id, lang) == label
