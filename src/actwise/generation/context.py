"""What the answering model reads: whole paragraphs, not the windows that retrieval ranks.

Retrieval ranks 150-word windows, so a long paragraph can reach the model in pieces and
out of order. A list read before the sentence that introduces it means something else
(docs/failure_cases.md, step 8b). The context takes the first distinct paragraphs of the
ranking instead, each whole and in the question's language.
"""

from __future__ import annotations

from collections.abc import Sequence

from actwise.ids import paragraph_id
from actwise.retrieval.passages import Hit, Passage, to_hit

MAX_PARAGRAPHS = 5  # as many sources as the windows gave (decision 004)
WORD_BUDGET = 2000  # the longest paragraph has 871 words; the median one, 69
POOL = 20  # windows fetched to find MAX_PARAGRAPHS distinct paragraphs


class ParagraphContext:
    """The first distinct paragraphs of a ranking, each whole, under a word budget."""

    def __init__(
        self,
        paragraphs: Sequence[Passage],
        max_paragraphs: int = MAX_PARAGRAPHS,
        word_budget: int = WORD_BUDGET,
        pool: int = POOL,
    ):
        """`paragraphs` holds every paragraph in each language, as `paragraph_passages()` gives."""
        self.paragraphs = {(p.id, p.lang): p for p in paragraphs}
        self.max_paragraphs, self.word_budget, self.pool = max_paragraphs, word_budget, pool

    def select(self, hits: Sequence[Hit], lang: str) -> list[Hit]:
        """The paragraphs of `hits`, best first: one copy each, in `lang` when it has one."""
        chosen: list[Hit] = []
        seen: set[str] = set()
        words = 0
        for hit in hits:
            pid = paragraph_id(hit.id)
            if pid in seen:
                continue
            seen.add(pid)
            paragraph = self.paragraphs.get((pid, lang)) or self.paragraphs[(pid, hit.lang)]
            size = len(paragraph.text.split())
            if words + size > self.word_budget:
                continue  # a shorter paragraph further down may still fit
            chosen.append(to_hit(paragraph, hit.score))
            words += size
            if len(chosen) == self.max_paragraphs:
                break
        return chosen
