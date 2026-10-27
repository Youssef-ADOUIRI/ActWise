"""Turn an uploaded system description (.txt, .md, .pdf, .docx) into plain text."""

from __future__ import annotations

import io
import logging
from collections.abc import Iterator
from pathlib import Path

import docx
from pypdf import PdfReader

log = logging.getLogger(__name__)


class UnsupportedFile(ValueError):
    """A file type that `extract_text` cannot read."""


def text_parts(data: bytes) -> Iterator[str]:
    """UTF-8 text, with or without a byte-order mark; bad bytes become U+FFFD."""
    yield data.decode("utf-8-sig", errors="replace")


def pdf_pages(data: bytes) -> Iterator[str]:
    """The text layer of each page, one page at a time (a scanned PDF has none)."""
    for page in PdfReader(io.BytesIO(data)).pages:
        yield page.extract_text() or ""


def docx_paragraphs(data: bytes) -> Iterator[str]:
    """Each paragraph of a Word document."""
    for paragraph in docx.Document(io.BytesIO(data)).paragraphs:
        yield paragraph.text


READERS = {".txt": text_parts, ".md": text_parts, ".pdf": pdf_pages, ".docx": docx_paragraphs}


def extract_text(filename: str, data: bytes, max_chars: int) -> str:
    """The file's text, cut to `max_chars`, or "" when the file cannot be parsed.

    Reading stops once `max_chars` characters are in, so the pages of a long PDF
    past the cut are never parsed. A type not in READERS raises UnsupportedFile.
    """
    suffix = Path(filename).suffix.lower()
    if suffix not in READERS:
        raise UnsupportedFile(f"unsupported file type {suffix!r}: use {', '.join(READERS)}")
    parts: list[str] = []
    size = 0
    try:
        for part in READERS[suffix](data):
            parts.append(part)
            size += len(part) + 1  # with the newline that joins it
            if size > max_chars:
                break
    except Exception:  # a broken upload: each parser fails in its own way
        log.info("an uploaded %s file could not be parsed", suffix)
        return ""
    return "\n".join(parts).strip()[:max_chars]
