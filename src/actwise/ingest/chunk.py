"""Units -> chunks with stable IDs, ready to embed and index."""

from __future__ import annotations

from dataclasses import asdict, dataclass

from actwise.ids import LAW_NAMES, storage_key
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
        return storage_key(self.id, self.lang)

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
        """The chunk as a plain dict: one line of chunks.jsonl."""
        return asdict(self)


def window_starts(n_words: int, max_words: int, overlap: int) -> list[int]:
    """Start of each window of `max_words` words; consecutive windows share `overlap` words."""
    if n_words <= max_words:
        return [0]
    step = max_words - overlap
    starts = []
    for start in range(0, n_words, step):
        starts.append(start)
        if start + max_words >= n_words:
            break
    return starts


def split_words(words: list[str], max_words: int, overlap: int) -> list[str]:
    """Words -> overlapping windows of text, placed by `window_starts()`."""
    starts = window_starts(len(words), max_words, overlap)
    return [" ".join(words[start : start + max_words]) for start in starts]


def unit_id(unit: Unit, law: str) -> str:
    """Article-level id of a unit, such as AIA-Art5: the level of the gold labels."""
    return f"{PREFIX[law]}-{TAG[unit.kind]}{unit.number}"


def law_of(chunk_id: str) -> str:
    """AIA-Art5-1 -> "ai_act": the law of a chunk id, as in `Chunk.law`."""
    code = chunk_id.split("-", 1)[0]
    return next(law for law, prefix in PREFIX.items() if prefix == code)


def chunk_units(
    units: list[Unit], law: str, lang: str, max_words: int = 150, overlap: int = 25
) -> list[Chunk]:
    """One chunk per paragraph (or per window of a long one), with its stable id."""
    chunks: list[Chunk] = []
    for unit in units:
        numbered = any(p.number for p in unit.paragraphs)
        base_id = unit_id(unit, law)

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
