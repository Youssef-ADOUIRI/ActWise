import pytest

from actwise.generation.context import ParagraphContext
from actwise.generation.prompts import load_prompt
from actwise.generation.rag import RagPipeline
from actwise.generation.rewrite import MAX_QUERIES, REWRITE_PROMPT, rewrite_queries
from actwise.llm.base import LLMResponse
from actwise.retrieval.passages import Passage, to_hit
from tests.unit.toys import ScriptedLLM

QUESTION = "Can a non-EU startup face fines under the AI Act?"
PARAGRAPHS = [
    Passage("AIA-Art2-1", "en", "AI Act Article 2(1)\nproviders established in a third country"),
    Passage("AIA-Art99-3", "en", "AI Act Article 99(3)\nadministrative fines of up to"),
]
FOUND = {  # query -> what the fake retriever returns
    QUESTION: [to_hit(PARAGRAPHS[1], 1.0)],
    "scope providers established in a third country": [to_hit(PARAGRAPHS[0], 1.0)],
    "penalties for infringements": [to_hit(PARAGRAPHS[1], 1.0)],
}


def reply(text):
    """A plain model reply."""
    return LLMResponse(text, [], 20, 10, "m")


def test_rewrite_queries_strips_bullets_and_caps_the_count():
    """Bullets, numbers and quotes go; blank lines are skipped; at most MAX_QUERIES remain."""
    llm = ScriptedLLM(reply('1. "scope of the regulation"\n\n- penalties\n* fines\n4) extra'))

    queries = rewrite_queries(llm, "Rewrite.", QUESTION, deadline=7.0)

    assert queries == ["scope of the regulation", "penalties", "fines"][:MAX_QUERIES]
    assert llm.calls[0]["messages"][1]["content"] == QUESTION
    assert llm.calls[0]["deadline"] == 7.0


def pipeline(llm, asked):
    """A rewriting pipeline whose fake retriever records every query."""

    def search(query, top_k):
        asked.append(query)
        return FOUND[query]

    return RagPipeline(
        llm, search, "Answer.", ParagraphContext(PARAGRAPHS), load_prompt(REWRITE_PROMPT)
    )


def test_a_refusal_is_retried_with_rewritten_queries():
    """Refused from the question's search, it is retried with the rewrite's queries alone, all
    under one deadline, and the second answer finds what the first search missed."""
    asked = []
    llm = ScriptedLLM(
        reply("NOT_COVERED"),
        reply("scope providers established in a third country\npenalties for infringements"),
        reply(
            "Yes, if it places systems on the EU market [AIA-Art2-1], fines apply [AIA-Art99-3]."
        ),
    )

    result = pipeline(llm, asked).ask(QUESTION, "en", deadline=42.0)

    assert asked == list(FOUND)  # the question, then both queries
    assert [s["id"] for s in result.sources] == ["AIA-Art2-1", "AIA-Art99-3"]
    assert (result.citations, result.retried) == (["AIA-Art2-1", "AIA-Art99-3"], True)
    assert [call["deadline"] for call in llm.calls] == [42.0, 42.0, 42.0]


def test_an_empty_rewrite_searches_the_question_again():
    """No query in the rewrite's reply: the retry searches the question, not nothing."""
    asked = []
    llm = ScriptedLLM(reply("NOT_COVERED"), reply("\n"), reply("NOT_COVERED"))

    result = pipeline(llm, asked).ask(QUESTION, "en")

    assert (asked, result.reason, result.retried) == ([QUESTION, QUESTION], "not_covered", True)


def test_an_answered_question_is_not_rewritten():
    """An answer on the first pass costs one search and one model call: no rewrite."""
    asked = []
    llm = ScriptedLLM(reply("Fines apply [AIA-Art99-3]."))

    result = pipeline(llm, asked).ask(QUESTION, "en")

    assert (asked, len(llm.calls), result.retried) == ([QUESTION], 1, False)


def test_a_rewrite_needs_a_paragraph_context():
    """Without a context, the pipeline reads the top windows of one search: no rewrite."""
    with pytest.raises(ValueError, match="context"):
        RagPipeline(ScriptedLLM(reply("x")), lambda q, k: [], "Answer.", None, "Rewrite.")
