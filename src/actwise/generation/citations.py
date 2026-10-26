"""Find the chunk ids an answer cites, and remove the ones that were not retrieved.

Citations are paragraph-level: `[AIA-Art3-12#2]` counts as a citation of AIA-Art3-12.
"""

from __future__ import annotations

import re

from actwise.ids import is_valid_id, paragraph_id

BRACKET = re.compile(r"(\s?)\[([^\[\]]+)\]")  # a [group], with the space before it
SENTENCE = re.compile(r"(?<=[.!?])\s+")


def _tokens(group: str) -> list[str]:
    """The comma-separated entries of one bracket group."""
    return [token.strip() for token in group.split(",")]


def extract_citations(answer: str) -> list[str]:
    """Valid ids cited in square brackets, as paragraph ids, in order of first use."""
    found: list[str] = []
    for _, group in BRACKET.findall(answer):
        for token in _tokens(group):
            cited = paragraph_id(token)
            if is_valid_id(cited) and cited not in found:  # `[1]` or `[note]` is not an id
                found.append(cited)
    return found


def invented_citations(answer: str, retrieved: set[str]) -> list[str]:
    """Cited ids that are not among the retrieved passages."""
    return [cited for cited in extract_citations(answer) if cited not in retrieved]


def uncited_sentences(answer: str) -> int:
    """How many sentences of the answer cite nothing."""
    return sum(1 for s in SENTENCE.split(answer.strip()) if s and not extract_citations(s))


def strip_citations(answer: str, ids: set[str]) -> str:
    """Remove these ids, matched whole, from their bracket groups (R2); an emptied group goes too.

    `str.replace` would also cut "AIA-Art6" out of a valid "[AIA-Art6-2]".
    """

    def keep_others(match: re.Match[str]) -> str:
        """The group without the removed ids, or nothing if none is left."""
        space, tokens = match.group(1), _tokens(match.group(2))
        kept = [t for t in tokens if paragraph_id(t) not in ids]
        if len(kept) == len(tokens):
            return match.group(0)
        return f"{space}[{', '.join(kept)}]" if kept else ""

    return BRACKET.sub(keep_others, answer)
