"""Answer golden questions, judge the answers, and render them for docs/generation.md.

The step 5 baseline prompt stays plain on purpose: no citation format and no refusal
rule, so the cited prompts have a "before" to beat.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import asdict
from typing import Any

from actwise.evaluation.golden import Question
from actwise.evaluation.judge import judge_answer
from actwise.generation.rag import CONTEXT_PASSAGES, AskResult, Search, sources_of
from actwise.llm.base import LLM, Message
from actwise.retrieval.passages import Passage

PLAIN_PROMPT = (
    "Answer the question using the context below.\n\nContext:\n{context}\n\nQuestion: {question}"
)

Ask = Callable[[str, str], AskResult]  # (question, lang) -> result, like RagPipeline.ask


def plain_messages(question: str, passages: Sequence[Passage]) -> list[Message]:
    """The baseline request: the passage texts, then the question, in one user message."""
    context = "\n\n".join(p.text for p in passages)
    return [{"role": "user", "content": PLAIN_PROMPT.format(context=context, question=question)}]


def plain_ask(llm: LLM, search: Search, question: str, lang: str) -> AskResult:
    """The baseline answer: no citation check and no refusal, at temperature 0."""
    hits = search(question, CONTEXT_PASSAGES)
    reply = llm.chat(plain_messages(question, hits), temperature=0)
    return AskResult(reply.text.strip(), "", [], [], sources_of(hits, lang), reply)


def quote(text: str) -> list[str]:
    """Markdown quote lines for a block of text; a blank line becomes a bare ">"."""
    return [f"> {line}".rstrip() for line in text.strip().splitlines()]


def answer_questions(
    ask: Ask, questions: list[Question], judge: LLM | None = None
) -> list[dict[str, Any]]:
    """One row per question, out-of-scope ones included; the judge scores each answer given."""
    rows: list[dict[str, Any]] = []
    for question in questions:
        result = ask(question.question, question.lang)
        reply = result.reply
        row = {
            "id": question.id,
            "lang": question.lang,
            "type": question.type,
            "question": question.question,
            "gold": list(question.gold),
            "answer": result.answer,
            "refused": result.refused,
            "reason": result.reason,
            "citations": result.citations,
            "invented": result.invented,
            "sources": result.sources,
            "model": reply.model if reply else "",
            "input_tokens": reply.input_tokens if reply else 0,
            "output_tokens": reply.output_tokens if reply else 0,
        }
        if judge is not None and not result.refused:
            verdict = judge_answer(judge, question.question, result.sources, result.answer)
            row["judge"] = asdict(verdict)
        rows.append(row)
    return rows


def answers_markdown(answers: dict[str, Any]) -> str:
    """Render the answers: the headline numbers, then each question and its quoted answer."""
    s = answers["summary"]
    lines = [
        "",
        f"## Answers: `{answers['prompt']}`",
        "",
        f"Top {CONTEXT_PASSAGES} passages, temperature 0, judge: {answers['judge'] or 'none'}.",
        "",
        "| Metric | Value |",
        "|---|---|",
    ]
    lines += [f"| {key} | {value} |" for key, value in s.items() if not isinstance(value, dict)]
    for row in answers["per_question"]:
        lines += ["", f"### {row['id']} ({row['lang']}, {row['type']})", ""]
        lines += [f"**Question:** {row['question']}", ""]
        status = f"refused ({row['reason']})" if row["refused"] else row["model"]
        lines += [f"**Answer** ({status}):", ""]
        lines += quote(row["answer"])
        if row["invented"]:
            lines += ["", f"Invented citations removed: {', '.join(row['invented'])}"]
        if verdict := row.get("judge"):
            lines += ["", f"Judge: {verdict['score']}/5. {verdict['reason']}"]
    return "\n".join(lines) + "\n"
