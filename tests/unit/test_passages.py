import json

from actwise.ingest.chunk import Chunk, law_of
from actwise.retrieval.passages import Passage, chunk_passages, to_hit


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
