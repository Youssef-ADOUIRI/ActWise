"""Stable chunk IDs shared by ingestion, retrieval, evaluation and citations.

Format: <LAW>-<Art|Annex|Rec><number>[-[<section>.]<paragraph>][#<part>]
Examples: AIA-Art6-2, AIA-AnnexIII-4, GDPR-Art17, AIA-Rec63, AIA-Art3-12#2,
AIA-AnnexVIII-b.1 (Annex VIII, Section B, point 1)

An ID never contains the language: the EN and FR versions of a paragraph
share one ID, so a French question is scored against the same gold article.
To store both languages side by side, use `Chunk.key` (`<id>@<lang>`).
"""

from __future__ import annotations

import re

ID_RE = re.compile(
    r"^(?P<law>[A-Z]+)-(?P<tag>Art|Annex|Rec)(?P<num>\d+|[IVXL]+)"
    r"(?:-(?P<para>(?:[0-9a-z]+\.)?[0-9a-z]+))?(?:#(?P<part>\d+))?$"
)

LAW_NAMES = {
    "en": {"AIA": "AI Act", "GDPR": "GDPR"},
    "fr": {"AIA": "Règlement IA", "GDPR": "RGPD"},
}


def parse_id(chunk_id: str) -> dict[str, str | None] | None:
    match = ID_RE.match(chunk_id.strip())
    return match.groupdict() if match else None


def is_valid_id(chunk_id: str) -> bool:
    return parse_id(chunk_id) is not None


def article_id(chunk_id: str) -> str:
    """AIA-Art6-2#1 -> AIA-Art6, the level used for gold labels."""
    parts = parse_id(chunk_id)
    if parts is None:
        raise ValueError(f"not a chunk id: {chunk_id!r}")
    return f"{parts['law']}-{parts['tag']}{parts['num']}"


def human_label(chunk_id: str, lang: str = "en") -> str:
    """AIA-Art6-2 -> 'AI Act, Art. 6(2)'. Shown to users, never sent to the model."""
    parts = parse_id(chunk_id)
    if parts is None:
        return chunk_id

    law_code, number, para = parts["law"] or "", parts["num"], parts["para"]
    law = LAW_NAMES.get(lang, LAW_NAMES["en"]).get(law_code, law_code)

    if parts["tag"] == "Art":
        suffix = f"({para})" if para and para != "0" else ""
        return f"{law}, Art. {number}{suffix}"
    if parts["tag"] == "Annex":
        word = "Annexe" if lang == "fr" else "Annex"
        return f"{law}, {word} {number}{_annex_point(para)}"
    word = "considérant" if lang == "fr" else "Recital"
    return f"{law}, {word} {number}"


def _annex_point(para: str | None) -> str:
    """'4' -> ', point 4'; 'b.1' -> ', Section B, point 1'; 'b.0' -> ', Section B'."""
    if not para:
        return ""
    if "." in para:
        section, point = para.split(".")
        return f", Section {section.upper()}" + (f", point {point}" if point != "0" else "")
    return f", point {para}"
