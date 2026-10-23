"""Answer golden questions from retrieved passages, and keep the answers for scoring in step 6.

The baseline prompt is plain on purpose: no citation format and no refusal rule,
so the cited prompts of step 6 have a "before" to beat.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Callable, Sequence
from typing import Any

from actwise.evaluation.golden import Question
from actwise.llm.base import LLM, Message
from actwise.retrieval.passages import Hit, Passage

PLAIN_PROMPT = (
    "Answer the question using the context below.\n\nContext:\n{context}\n\nQuestion: {question}"
)
CONTEXT_PASSAGES = 5  # the generator reads the top 5 passages (decision 004)


def plain_messages(question: str, passages: Sequence[Passage]) -> list[Message]:
    """The baseline request: the passage texts, then the question, in one user message."""
    context = "\n\n".join(p.text for p in passages)
    return [{"role": "user", "content": PLAIN_PROMPT.format(context=context, question=question)}]


def answer_questions(
    llm: LLM,
    search: Callable[[str, int], list[Hit]],
    questions: list[Question],
    top_k: int = CONTEXT_PASSAGES,
) -> dict[str, Any]:
    """Answer every question, out-of-scope ones included, at temperature 0: one row each."""
    rows: list[dict[str, Any]] = []
    for question in questions:
        hits = search(question.question, top_k)
        response = llm.chat(plain_messages(question.question, hits), temperature=0)
        rows.append(
            {
                "id": question.id,
                "lang": question.lang,
                "type": question.type,
                "question": question.question,
                "passages": [hit.key for hit in hits],
                "answer": response.text,
                "model": response.model,
                "input_tokens": response.input_tokens,
                "output_tokens": response.output_tokens,
            }
        )
    summary = {
        "n": len(rows),
        "models": dict(Counter(row["model"] for row in rows)),
        "input_tokens": sum(row["input_tokens"] for row in rows),
        "output_tokens": sum(row["output_tokens"] for row in rows),
    }
    return {"prompt": PLAIN_PROMPT, "top_k": top_k, "summary": summary, "per_question": rows}


def answers_markdown(answers: dict[str, Any]) -> str:
    """Render the answers as Markdown: a summary line, then each question and its quoted answer."""
    s = answers["summary"]
    models = ", ".join(f"{model} ({n})" for model, n in s["models"].items())
    lines = [
        "",
        "## Answers",
        "",
        f"Plain prompt, top {answers['top_k']} passages, temperature 0. {s['n']} answers by "
        f"{models}; {s['input_tokens']:,} input and {s['output_tokens']:,} output tokens.",
    ]
    for row in answers["per_question"]:
        lines += [
            "",
            f"### {row['id']} ({row['lang']}, {row['type']})",
            "",
            f"**Question:** {row['question']}",
            "",
            f"**Answer** ({row['model']}):",
            "",
        ]
        lines += [f"> {line}".rstrip() for line in row["answer"].strip().splitlines()]
    return "\n".join(lines) + "\n"
