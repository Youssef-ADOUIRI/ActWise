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


def test_the_pipeline_searches_every_query_and_shares_the_deadline():
    """The rewrite's queries find what the question alone missed; both calls get the deadline."""
    asked = []
    llm = ScriptedLLM(
        reply("scope providers established in a third country\npenalties for infringements"),
        reply(
            "Yes, if it places systems on the EU market [AIA-Art2-1], fines apply [AIA-Art99-3]."
        ),
    )

    def search(query, top_k):
        asked.append(query)
        return FOUND[query]

    context = ParagraphContext(PARAGRAPHS)
    result = RagPipeline(llm, search, "Answer.", context, load_prompt(REWRITE_PROMPT)).ask(
        QUESTION, "en", deadline=42.0
    )

    assert asked == list(FOUND)
    assert [s["id"] for s in result.sources] == ["AIA-Art99-3", "AIA-Art2-1"]
    assert result.citations == ["AIA-Art2-1", "AIA-Art99-3"]
    assert [call["deadline"] for call in llm.calls] == [42.0, 42.0]


def test_a_rewrite_needs_a_paragraph_context():
    """Without a context, the pipeline reads the top windows of one search: no rewrite."""
    with pytest.raises(ValueError, match="context"):
        RagPipeline(ScriptedLLM(reply("x")), lambda q, k: [], "Answer.", None, "Rewrite.")
