from actwise.ingest.chunk import chunk_units
from actwise.ingest.parse import Paragraph, Unit, parse_regulation
from tests.unit.sample_text import EN_SAMPLE, EXPECTED_IDS, FR_SAMPLE


def en_chunks():
    return chunk_units(parse_regulation(EN_SAMPLE), law="ai_act", lang="en")


def test_chunk_ids():
    ids = [c.id for c in en_chunks()]

    assert ids == EXPECTED_IDS
    assert len(set(ids)) == len(ids)


def test_embed_text_header():
    chunk = next(c for c in en_chunks() if c.id == "AIA-Art5-1")

    assert chunk.embed_text.startswith("AI Act Article 5(1): Prohibited AI practices\n")


def test_french_header_uses_french_names():
    chunks = chunk_units(parse_regulation(FR_SAMPLE), law="ai_act", lang="fr")
    chunk = next(c for c in chunks if c.id == "AIA-AnnexIII-4")

    assert chunk.embed_text.startswith("Règlement IA Annexe III(4):")


def test_same_ids_in_french():
    fr_ids = [c.id for c in chunk_units(parse_regulation(FR_SAMPLE), law="ai_act", lang="fr")]

    assert fr_ids == EXPECTED_IDS


def test_storage_key_keeps_languages_apart():
    en = en_chunks()[0]
    fr = chunk_units(parse_regulation(FR_SAMPLE), law="ai_act", lang="fr")[0]

    assert en.id == fr.id
    assert en.key != fr.key


def test_long_paragraph_split():
    words = [f"w{i}" for i in range(400)]
    unit = Unit("article", "9", "Risk management", [Paragraph("1", " ".join(words))])

    chunks = chunk_units([unit], law="ai_act", lang="en", max_words=150, overlap=25)

    assert [c.id for c in chunks] == ["AIA-Art9-1#1", "AIA-Art9-1#2", "AIA-Art9-1#3"]
    pieces = [c.text.split() for c in chunks]
    for left, right in zip(pieces, pieces[1:], strict=False):
        assert left[-25:] == right[:25]
    assert {w for piece in pieces for w in piece} == set(words)
