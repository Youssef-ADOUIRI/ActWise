import pytest

from actwise.evaluation.judge import Verdict, judge_answer, parse_verdict
from actwise.llm.base import LLMResponse
from tests.unit.toys import ScriptedLLM

SOURCES = [{"id": "AIA-Art5-1", "text": "The following AI practices shall be prohibited..."}]


def test_parse_verdict_reads_json_inside_a_code_fence():
    """The JSON object is found even when the judge wraps it in prose or a fence."""
    verdict = '{"score": 4, "reason": "One detail.", "unsupported_citations": ["[AIA-Art9-1]"]}'
    reply = f"Here you go:\n```json\n{verdict}\n```"

    assert parse_verdict(reply) == Verdict(4, "One detail.", ["AIA-Art9-1"])


@pytest.mark.parametrize("reply", ["no json here", '{"score": 7}', '{"score": "high"}', "[1, 2]"])
def test_unreadable_verdicts_have_no_score(reply):
    """A reply without a valid 1–5 score is kept as unreadable, never as a silent 0."""
    assert parse_verdict(reply).score is None


def test_judge_answer_sends_sources_question_and_answer():
    """The judge sees each source under its id, then the question and the answer."""
    llm = ScriptedLLM(LLMResponse('{"score": 5, "reason": "ok"}', [], 1, 1, "judge"))

    verdict = judge_answer(llm, "What is banned?", SOURCES, "Social scoring [AIA-Art5-1].")

    user = llm.calls[0]["messages"][1]["content"]
    assert "[AIA-Art5-1]\nThe following" in user and user.endswith("Social scoring [AIA-Art5-1].")
    assert verdict.score == 5 and llm.calls[0]["temperature"] == 0
