"""Turn an uploaded system description (.txt, .md, .pdf, .docx) into plain text."""

from __future__ import annotations

import io
import logging
from pathlib import Path

import docx
from pypdf import PdfReader

log = logging.getLogger(__name__)


class UnsupportedFile(ValueError):
    """A file type that `extract_text` cannot read."""


def read_text(data: bytes) -> str:
    """UTF-8 text, with or without a byte-order mark; bad bytes become U+FFFD."""
    return data.decode("utf-8-sig", errors="replace")


def read_pdf(data: bytes) -> str:
    """The text layer of every page (a scanned PDF has none)."""
    return "\n".join(page.extract_text() or "" for page in PdfReader(io.BytesIO(data)).pages)


def read_docx(data: bytes) -> str:
    """Every paragraph of a Word document."""
    return "\n".join(p.text for p in docx.Document(io.BytesIO(data)).paragraphs)


READERS = {".txt": read_text, ".md": read_text, ".pdf": read_pdf, ".docx": read_docx}


def extract_text(filename: str, data: bytes, max_chars: int) -> str:
    """The file's text, cut to `max_chars`, or "" when the file cannot be parsed.

    A type other than those of READERS raises UnsupportedFile.
    """
    suffix = Path(filename).suffix.lower()
    if suffix not in READERS:
        raise UnsupportedFile(f"unsupported file type {suffix!r}: use {', '.join(READERS)}")
    try:
        text = READERS[suffix](data)
    except Exception:  # a broken upload: each parser fails in its own way
        log.info("an uploaded %s file could not be parsed", suffix)
        return ""
    return text.strip()[:max_chars]
