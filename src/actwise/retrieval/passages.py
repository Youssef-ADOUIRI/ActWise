"""What every retriever indexes and returns: passages, and hits with a score."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from actwise.ids import storage_key
from actwise.ingest.build_chunks import OUT_FILE, load_chunks
from actwise.ingest.chunk import law_of


@dataclass(frozen=True)
class Passage:
    """A text to retrieve. `id` is the language-free chunk id that metrics and citations use."""

    id: str
    lang: str
    text: str

    @property
    def key(self) -> str:
        """Storage key `id@lang`: the EN and FR versions of a passage share an `id`."""
        return storage_key(self.id, self.lang)

    @property
    def payload(self) -> dict[str, str]:
        """What a store keeps next to the vector; `where` filters match these fields."""
        return {"key": self.key, "id": self.id, "law": law_of(self.id), "lang": self.lang}


@dataclass(frozen=True)
class Hit(Passage):
    score: float


def to_hit(passage: Passage, score: float) -> Hit:
    """The passage with its retrieval score."""
    return Hit(passage.id, passage.lang, passage.text, score)


def chunk_passages(chunk_file: Path = OUT_FILE) -> list[Passage]:
    """Structure-aware passages: one per chunk, with its header (`Chunk.embed_text`)."""
    return [Passage(c.id, c.lang, c.embed_text) for c in load_chunks(chunk_file)]
