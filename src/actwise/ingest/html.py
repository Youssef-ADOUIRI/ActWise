"""Saved EUR-Lex HTML page -> plain text, one block of text per line."""

from __future__ import annotations

import warnings
from pathlib import Path

from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning

NOISE_TAGS = ["script", "style", "nav", "header", "footer"]


def html_string_to_text(html: str) -> str:
    """HTML -> text without the `NOISE_TAGS` elements, one block per line."""
    with warnings.catch_warnings():
        # EUR-Lex serves XHTML with an XML declaration; the HTML parser handles it fine.
        warnings.simplefilter("ignore", XMLParsedAsHTMLWarning)
        soup = BeautifulSoup(html, "lxml")
    for tag in soup(NOISE_TAGS):
        tag.decompose()
    # EUR-Lex writes "Article&nbsp;6"; a plain space keeps later regexes simple.
    return soup.get_text("\n").replace("\xa0", " ")


def html_to_text(path: str | Path) -> str:
    """Read a saved page (UTF-8) and convert it with `html_string_to_text()`."""
    return html_string_to_text(Path(path).read_text(encoding="utf-8"))
