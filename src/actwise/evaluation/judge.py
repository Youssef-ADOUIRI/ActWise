"""An LLM judge for faithfulness: does every claim of an answer come from its sources?"""

from __future__ import annotations

from dataclasses import dataclass

from actwise.generation.prompts import json_object, load_prompt
from actwise.generation.rag import format_sources
from actwise.llm.base import LLM, Message

JUDGE_PROMPT = "judge.v1"
JUDGE_MAX_TOKENS = 2048  # a thinking model spends part of it reasoning before the JSON


@dataclass(frozen=True)
class Verdict:
    score: int | None  # 1 to 5; None when the judge's reply could not be read
    reason: str
    unsupported: list[str]  # cited ids whose source does not support their sentence


def parse_verdict(reply: str) -> Verdict:
    """Read the judge's JSON; a reply without a 1–5 score gives `score=None`, never a 0."""
    data = json_object(reply) or {}
    score = data.get("score")
    if isinstance(score, bool) or score not in (1, 2, 3, 4, 5):
        return Verdict(None, f"unreadable judge reply: {reply[:200]!r}", [])
    unsupported = [str(c).strip("[] ") for c in data.get("unsupported_citations") or []]
    return Verdict(int(score), str(data.get("reason", "")), unsupported)


def judge_messages(question: str, sources: list[dict[str, str]], answer: str) -> list[Message]:
    """The judge prompt, then the sources as the answerer saw them, the question and the answer."""
    user = f"Sources:\n\n{format_sources(sources)}\n\nQuestion: {question}\n\nAnswer: {answer}"
    return [
        {"role": "system", "content": load_prompt(JUDGE_PROMPT)},
        {"role": "user", "content": user},
    ]


def judge_answer(llm: LLM, question: str, sources: list[dict[str, str]], answer: str) -> Verdict:
    """Score one answer against the passages it was written from."""
    messages = judge_messages(question, sources, answer)
    return parse_verdict(llm.chat(messages, temperature=0, max_tokens=JUDGE_MAX_TOKENS).text)
