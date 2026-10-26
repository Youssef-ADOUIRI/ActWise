from functools import partial

from actwise.evaluation.answers import (
    answer_questions,
    answers_markdown,
    plain_ask,
    plain_messages,
)
from actwise.evaluation.golden import Question
from actwise.generation.rag import RagPipeline
from actwise.llm.base import LLMResponse
from actwise.retrieval.passages import to_hit
from tests.unit.toys import PASSAGES, ScriptedLLM

QUESTIONS = [
    Question("q1", "en", "lookup", "Which practices are banned?", ("AIA-Art5",), "..."),
    Question("q2", "fr", "not_covered", "Que dit le DMA ?", (), "...", split="dev"),
]
ANSWER = LLMResponse("Article 5 bans them.\n\n- social scoring", [], 100, 10, "gemini-x")
VERDICT = LLMResponse('{"score": 4, "reason": "One detail is missing."}', [], 1, 1, "judge-x")


def search(query, top_k):
    """Fake retriever: the toy passages in their order."""
    return [to_hit(p, 1.0) for p in PASSAGES[:top_k]]


def test_plain_prompt_holds_the_passages_then_the_question():
    """One user message: each passage text, then the question; nothing about citations."""
    [message] = plain_messages("Which practices are banned?", PASSAGES[:2])

    assert message["role"] == "user"
    assert PASSAGES[0].text in message["content"] and PASSAGES[1].text in message["content"]
    assert message["content"].endswith("Question: Which practices are banned?")
    assert "cit" not in message["content"].lower()


def test_plain_answers_are_never_refused_and_record_their_model():
    """The baseline answers every question, out-of-scope ones too, at temperature 0."""
    llm = ScriptedLLM(ANSWER)

    rows = answer_questions(partial(plain_ask, llm, search), QUESTIONS)

    assert [(r["id"], r["refused"], r["model"]) for r in rows] == [
        ("q1", False, "gemini-x"),
        ("q2", False, "gemini-x"),
    ]
    assert [s["key"] for s in rows[0]["sources"][:2]] == ["GDPR-Art17-1@en", "AIA-Art5-1@en"]
    assert [call["temperature"] for call in llm.calls] == [0, 0]


def test_the_judge_scores_answers_but_not_refusals():
    """A refused question gets no verdict; an answered one gets the judge's score."""
    rag = RagPipeline(ScriptedLLM(LLMResponse("NOT_COVERED", [], 1, 1, "m")), search, "rules")
    judge = ScriptedLLM(VERDICT)

    rows = answer_questions(rag.ask, QUESTIONS, judge)
    plain = answer_questions(partial(plain_ask, ScriptedLLM(ANSWER), search), QUESTIONS[:1], judge)

    assert "judge" not in rows[0] and rows[0]["reason"] == "not_covered"
    assert plain[0]["judge"]["score"] == 4


def test_answers_markdown_quotes_each_answer():
    """Each question gets a heading, its quoted answer and the judge's verdict."""
    rows = answer_questions(
        partial(plain_ask, ScriptedLLM(ANSWER), search), QUESTIONS, ScriptedLLM(VERDICT)
    )
    answers = {"prompt": "plain", "judge": "judge-x", "summary": {"n": 2}, "per_question": rows}

    text = answers_markdown(answers)

    assert "### q2 (fr, not_covered)" in text
    assert "> Article 5 bans them.\n>\n> - social scoring" in text
    assert "Judge: 4/5. One detail is missing." in text
