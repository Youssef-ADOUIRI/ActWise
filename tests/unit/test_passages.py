import json

from actwise.ingest.chunk import WINDOW_OVERLAP, WINDOW_WORDS, Chunk, law_of, split_words
from actwise.retrieval.passages import Passage, chunk_passages, paragraph_passages, to_hit


def test_payload_names_the_law_and_the_storage_key():
    """Stores filter on these fields, and find the passage again by its key."""
    passage = Passage("GDPR-Art17-1", "fr", "Droit à l’effacement")

    assert passage.payload == {
        "key": "GDPR-Art17-1@fr",
        "id": "GDPR-Art17-1",
        "law": "gdpr",
        "lang": "fr",
    }
    assert law_of("AIA-AnnexIII-4") == "ai_act"


def test_chunk_passages_carry_the_header(tmp_path):
    """Structure-aware passages embed the chunk header, as BM25 and the embedder see it."""
    chunk = Chunk("GDPR-Art17-1", "gdpr", "en", "article", "17", "1", "Right to erasure", "Text.")
    path = tmp_path / "chunks.jsonl"
    path.write_text(json.dumps(chunk.to_json()) + "\n", encoding="utf-8")

    (passage,) = chunk_passages(path)

    assert passage.text == "GDPR Article 17(1): Right to erasure\nText."
    assert to_hit(passage, 0.5).key == "GDPR-Art17-1@en"


def test_paragraph_passages_join_windows_without_the_overlap(tmp_path):
    """A paragraph cut into windows comes back whole: one header, shared words once."""
    words = [f"w{i}" for i in range(200)]
    parts = split_words(words, WINDOW_WORDS, WINDOW_OVERLAP)
    chunks = [
        Chunk(f"AIA-Art9-2#{n}", "ai_act", "en", "article", "9", "2", "Risk", text, n)
        for n, text in enumerate(parts, start=1)
    ]
    path = tmp_path / "chunks.jsonl"
    path.write_text("".join(json.dumps(c.to_json()) + "\n" for c in chunks), encoding="utf-8")

    [passage] = paragraph_passages(path)

    assert len(parts) == 2 and passage.id == "AIA-Art9-2"
    assert passage.text == "AI Act Article 9(2): Risk\n" + " ".join(words)
