"""Cheap input guardrails: they cut noise; the sources and the citation check are the defence."""

from __future__ import annotations

import re

EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
PHONE = re.compile(r"(?<!\w)\+?\d[\d .()/-]{7,}\d(?!\w)")
INJECTION = re.compile(
    r"(ignore (all |your |the )?(previous|prior|above) (instructions|rules)"
    r"|disregard (the )?(system|previous) (prompt|instructions)"
    r"|reveal (your|the) (system )?prompt"
    r"|oublie (tes|toutes les|les) (instructions|consignes)"
    r"|ignore (tes|les|toutes les) (instructions|consignes)( précédentes)?)",
    re.IGNORECASE,
)


def redact_pii(text: str) -> str:
    """Replace emails and phone numbers; applied before a question is logged or traced."""
    return PHONE.sub("[phone]", EMAIL.sub("[email]", text))


def looks_like_injection(text: str) -> bool:
    """True when the text tries to override the instructions, in English or French."""
    return bool(INJECTION.search(text))
