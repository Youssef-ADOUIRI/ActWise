import codecs
import io

import docx
import pytest

from actwise.ingest.files import UnsupportedFile, extract_text


def word_file(*paragraphs):
    """A .docx file holding these paragraphs."""
    document = docx.Document()
    for text in paragraphs:
        document.add_paragraph(text)
    buffer = io.BytesIO()
    document.save(buffer)
    return buffer.getvalue()


def test_extract_text():
    """TXT and DOCX give their text, cut at `max_chars`; a broken file gives none; .exe raises."""
    word = word_file("A chatbot for customers.", "It says that it is an AI.")

    assert extract_text("system.TXT", codecs.BOM_UTF8 + b"A CV-screening tool.\n", 100) == (
        "A CV-screening tool."
    )
    assert (
        extract_text("system.docx", word, 100)
        == "A chatbot for customers.\nIt says that it is an AI."
    )
    assert extract_text("long.md", b"x" * 50, 20) == "x" * 20
    assert extract_text("broken.pdf", b"not a pdf", 100) == ""
    with pytest.raises(UnsupportedFile):
        extract_text("setup.exe", b"MZ", 100)
