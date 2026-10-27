"""What every retriever indexes and returns: passages, and hits with a score."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from actwise.ids import paragraph_id, storage_key
from actwise.ingest.build_chunks import OUT_FILE, load_chunks
from actwise.ingest.chunk import WINDOW_OVERLAP, Chunk, law_of


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


def paragraph_passages(chunk_file: Path = OUT_FILE) -> list[Passage]:
    """One passage per paragraph and language: a long paragraph's windows joined back, one header.

    Consecutive windows share `WINDOW_OVERLAP` words, which are dropped again here.
    """
    groups: dict[tuple[str, str], list[Chunk]] = {}
    for chunk in load_chunks(chunk_file):
        groups.setdefault((paragraph_id(chunk.id), chunk.lang), []).append(chunk)
    passages = []
    for (pid, lang), parts in groups.items():
        parts.sort(key=lambda chunk: chunk.part)
        words = parts[0].text.split()
        for part in parts[1:]:
            words += part.text.split()[WINDOW_OVERLAP:]
        header = parts[0].embed_text.split("\n", 1)[0]
        passages.append(Passage(pid, lang, f"{header}\n{' '.join(words)}"))
    return passages
