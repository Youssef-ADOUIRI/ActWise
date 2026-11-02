"""What the answering model reads: whole paragraphs, not the windows that retrieval ranks.

Retrieval ranks 150-word windows, so a long paragraph can reach the model in pieces and
out of order. A list read before the sentence that introduces it means something else
(docs/failure_cases.md, step 8b). The context takes the first distinct paragraphs of the
ranking instead, each whole and in the question's language.

It can also follow what those paragraphs refer to: a point of an annex, a one-unit annex
(Art. 5(1)(h)(iii) needs the offences of Annex II), or another paragraph of the same
article. "Article N" is not followed: most paragraphs cite one, and the context would flood.
"""

from __future__ import annotations

import re
from collections.abc import Sequence

from actwise.ids import article_id, paragraph_id
from actwise.retrieval.passages import Hit, Passage, to_hit

MAX_PARAGRAPHS = 5  # as many sources as the windows gave (decision 004)
WORD_BUDGET = 2000  # the longest paragraph has 871 words; the median one, 69
POOL = 20  # windows fetched to find MAX_PARAGRAPHS distinct paragraphs
MAX_REFERENCES = 3  # units added because a chosen paragraph names them
# Read in the English copy: French writes "article 6, paragraphe 2" for another article.
POINTS = re.compile(r"\bpoints? ([\d\s(),a-z]+?) of Annex ([IVXL]+)\b")
ANNEX = re.compile(r"\bAnnex ([IVXL]+)\b")
PARAGRAPHS = re.compile(r"\bparagraphs? (\d+(?:(?:, | and | or )\d+)*)(?!\d| of (?!this Article))")


class ParagraphContext:
    """The first distinct paragraphs of a ranking, each whole, under a word budget."""

    def __init__(
        self,
        paragraphs: Sequence[Passage],
        max_paragraphs: int = MAX_PARAGRAPHS,
        word_budget: int = WORD_BUDGET,
        pool: int = POOL,
        max_references: int = 0,
        main_paragraphs: bool = False,
    ):
        """`paragraphs` holds every paragraph in each language, as `paragraph_passages()` gives.

        With `max_references`, up to that many units named by the chosen paragraphs follow.
        With `main_paragraphs`, a later paragraph of an article brings the article's first
        one, which usually states the rule that the others qualify.
        """
        self.paragraphs = {(p.id, p.lang): p for p in paragraphs}
        self.max_paragraphs, self.word_budget, self.pool = max_paragraphs, word_budget, pool
        self.max_references, self.main_paragraphs = max_references, main_paragraphs

    def references(self, pid: str) -> list[str]:
        """The annex units and same-article paragraphs that paragraph `pid` names, in order."""
        english = self.paragraphs.get((pid, "en"))
        if english is None:
            return []
        body, law = english.text.split("\n", 1)[-1], pid.split("-")[0]  # no header
        found = [
            f"{law}-Annex{annex}-{n}"
            for numbers, annex in POINTS.findall(body)
            for n in re.findall(r"\d+", numbers)
        ]
        found += [f"{law}-Annex{annex}" for annex in ANNEX.findall(body)]
        found += [
            f"{article_id(pid)}-{n}"
            for numbers in PARAGRAPHS.findall(body)
            for n in re.findall(r"\d+", numbers)
        ]
        return [ref for ref in dict.fromkeys(found) if (ref, "en") in self.paragraphs]

    def select(self, hits: Sequence[Hit], lang: str) -> list[Hit]:
        """The paragraphs of `hits`, best first: one copy each, in `lang` when it has one.

        Then their articles' first paragraphs (with `main_paragraphs`) and the units they
        name (up to `max_references`), as long as the budget allows.
        """
        chosen: list[Hit] = []
        seen: set[str] = set()
        words = 0

        def add(pid: str, fallback_lang: str, score: float) -> bool:
            """Add a paragraph if it fits the budget; True when it was added."""
            nonlocal words
            seen.add(pid)
            paragraph = self.paragraphs.get((pid, lang)) or self.paragraphs[(pid, fallback_lang)]
            size = len(paragraph.text.split())
            if words + size > self.word_budget:
                return False  # a shorter paragraph further down may still fit
            chosen.append(to_hit(paragraph, score))
            words += size
            return True

        for hit in hits:
            if len(chosen) == self.max_paragraphs:
                break
            if (pid := paragraph_id(hit.id)) not in seen:
                add(pid, hit.lang, hit.score)
        ranked = list(chosen)
        if self.main_paragraphs:
            for hit in ranked:
                first = f"{article_id(hit.id)}-1"
                if "-Art" in hit.id and first not in seen and (first, "en") in self.paragraphs:
                    add(first, "en", 0.0)
        named = [ref for hit in ranked for ref in self.references(hit.id)]
        added = 0
        for ref in named:
            if added == self.max_references:
                break
            if ref not in seen:
                added += add(ref, "en", 0.0)
        return chosen
