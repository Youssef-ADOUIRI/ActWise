from actwise.evaluation.answers import answer_questions, answers_markdown, plain_messages
from actwise.evaluation.golden import Question
from actwise.llm.base import LLMResponse
from actwise.retrieval.passages import to_hit
from tests.unit.toys import PASSAGES, ScriptedLLM

QUESTIONS = [
    Question("q1", "en", "lookup", "Which practices are banned?", ("AIA-Art5",), "..."),
    Question("q2", "fr", "not_covered", "Que dit le DMA ?", (), "...", split="dev"),
]
ANSWER = LLMResponse("Article 5 bans them.\n\n- social scoring", [], 100, 10, "gemini-x")


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


def test_every_question_is_answered_and_its_model_recorded():
    """Out-of-scope questions are answered too, at temperature 0, from the top passages."""
    llm = ScriptedLLM(ANSWER)

    answers = answer_questions(llm, search, QUESTIONS, top_k=2)

    rows = answers["per_question"]
    assert [row["id"] for row in rows] == ["q1", "q2"]
    assert rows[0]["passages"] == ["GDPR-Art17-1@en", "AIA-Art5-1@en"]
    assert (rows[0]["answer"], rows[0]["model"]) == (ANSWER.text, "gemini-x")
    assert answers["summary"] == {
        "n": 2,
        "models": {"gemini-x": 2},
        "input_tokens": 200,
        "output_tokens": 20,
    }
    assert [call["temperature"] for call in llm.calls] == [0, 0]


def test_answers_markdown_quotes_each_answer():
    """Each question gets a heading, and its answer is quoted line by line."""
    text = answers_markdown(answer_questions(ScriptedLLM(ANSWER), search, QUESTIONS, top_k=2))

    assert "### q2 (fr, not_covered)" in text
    assert "> Article 5 bans them.\n>\n> - social scoring" in text
