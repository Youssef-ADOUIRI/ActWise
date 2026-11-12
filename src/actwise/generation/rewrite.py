"""Search queries in the law's words: one model call before retrieval (step 8b).

Questions use everyday words ("non-EU", "presence"); the law uses its own ("third
country", "established or located"). A rewrite closes that gap, and one query per part of
the question lets an answer that needs two articles find both.
"""

from __future__ import annotations

import re

from actwise.llm.base import LLM

REWRITE_PROMPT = "rewrite.v1"
MAX_QUERIES = 3
BULLET = re.compile(r"^\s*(?:[-*•]|\d+[.)])\s*")


def rewrite_queries(
    llm: LLM, prompt: str, question: str, deadline: float | None = None
) -> list[str]:
    """Up to MAX_QUERIES search queries for `question`: the reply's lines, bullets removed."""
    reply = llm.chat(
        [{"role": "system", "content": prompt}, {"role": "user", "content": question}],
        temperature=0,
        deadline=deadline,
    )
    lines = (BULLET.sub("", line).strip().strip('"') for line in reply.text.splitlines())
    return [line for line in lines if line][:MAX_QUERIES]
