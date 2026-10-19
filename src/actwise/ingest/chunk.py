"""Units -> chunks with stable IDs, ready to embed and index."""

from __future__ import annotations

from dataclasses import asdict, dataclass

from actwise.ids import LAW_NAMES
from actwise.ingest.parse import Unit

PREFIX = {"ai_act": "AIA", "gdpr": "GDPR"}
TAG = {"recital": "Rec", "article": "Art", "annex": "Annex"}
KIND_WORD = {
    "en": {"recital": "Recital", "article": "Article", "annex": "Annex"},
    "fr": {"recital": "Considérant", "article": "Article", "annex": "Annexe"},
}


@dataclass(frozen=True)
class Chunk:
    id: str  # language-free, used for citations and metrics
    law: str  # "ai_act" | "gdpr"
    lang: str  # "en" | "fr"
    kind: str  # "recital" | "article" | "annex"
    number: str
    paragraph: str | None
    title: str
    text: str
    part: int = 1

    @property
    def key(self) -> str:
        """Storage key. EN and FR share an `id`, so stores must use this instead."""
        return f"{self.id}@{self.lang}"

    @property
    def embed_text(self) -> str:
        """Header + text: what the embedder and BM25 actually see."""
        law = LAW_NAMES[self.lang][PREFIX[self.law]]
        word = KIND_WORD[self.lang][self.kind]
        para = f"({self.paragraph})" if self.paragraph and self.paragraph != "0" else ""
        header = f"{law} {word} {self.number}{para}"
        if self.title:
            header += f": {self.title}"
        return f"{header}\n{self.text}"

    def to_json(self) -> dict:
        return asdict(self)


def split_words(words: list[str], max_words: int, overlap: int) -> list[str]:
    """Windows of `max_words` words; consecutive windows share `overlap` words."""
    if len(words) <= max_words:
        return [" ".join(words)]
    step = max_words - overlap
    windows = []
    for start in range(0, len(words), step):
        windows.append(" ".join(words[start : start + max_words]))
        if start + max_words >= len(words):
            break
    return windows


def chunk_units(
    units: list[Unit], law: str, lang: str, max_words: int = 150, overlap: int = 25
) -> list[Chunk]:
    chunks: list[Chunk] = []
    for unit in units:
        numbered = any(p.number for p in unit.paragraphs)
        base_id = f"{PREFIX[law]}-{TAG[unit.kind]}{unit.number}"

        for paragraph in unit.paragraphs:
            # An intro sentence before numbered paragraphs becomes paragraph "0".
            para = paragraph.number or ("0" if numbered else None)
            pieces = split_words(paragraph.text.split(), max_words, overlap)

            for part, piece in enumerate(pieces, start=1):
                chunk_id = base_id + (f"-{para}" if para else "")
                if len(pieces) > 1:
                    chunk_id += f"#{part}"
                chunks.append(
                    Chunk(
                        id=chunk_id,
                        law=law,
                        lang=lang,
                        kind=unit.kind,
                        number=unit.number,
                        paragraph=para,
                        title=unit.title,
                        text=piece,
                        part=part,
                    )
                )
    return chunks
