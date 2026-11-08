from actwise.ingest.chunk import Chunk
from actwise.llm.base import LLMResponse
from actwise.training.pairs import draft_pair, make_pairs, review_sample
from tests.unit.toys import ScriptedLLM


def chunk(cid, lang="en", text="the provider keeps the logs for six months at least"):
    """A toy article chunk long enough to be picked."""
    return Chunk(cid, "ai_act", lang, "article", "5", "1", "", f"{text} {lang} " + "mot " * 25)


def reply(en, fr):
    """A model reply holding one question per language."""
    return LLMResponse(f'{{"en": "{en}", "fr": "{fr}"}}', [], 1, 1, "m")


CHUNKS = [chunk(i, lang) for i in ("AIA-Art5-1", "AIA-Art9-1#1") for lang in ("en", "fr")]
CHUNKS += [chunk("AIA-Art7-1"), chunk("AIA-Art7-1", "fr")]
SPLIT = {"AIA-Art5": "train", "AIA-Art9": "train", "AIA-Art7": "test"}


def test_draft_pair_asks_once_for_both_languages():
    """One call reads the passage and returns a question per language."""
    llm = ScriptedLLM(reply("Who keeps the logs?", "Qui conserve les journaux ?"))

    draft = draft_pair(llm, chunk("AIA-Art5-1"))

    assert draft == {"en": "Who keeps the logs?", "fr": "Qui conserve les journaux ?"}
    assert "Passage:\nAI Act" in llm.calls[0]["messages"][1]["content"]
    assert len(llm.calls) == 1


def test_an_unreadable_reply_gives_empty_questions():
    """A reply without JSON drafts nothing, and the screen drops it."""
    llm = ScriptedLLM(LLMResponse("Sorry, I can't.", [], 1, 1, "m"))

    assert draft_pair(llm, chunk("AIA-Art5-1")) == {"en": "", "fr": ""}


def test_make_pairs_keeps_each_question_with_its_own_language():
    """French pairs only for single-window paragraphs; test articles are never drafted."""
    llm = ScriptedLLM(
        reply("Who must keep the logs and for how long?", "Qui doit conserver les journaux ?"),
        reply("How long are the logs kept by providers?", "Combien de temps garder ?"),
    )

    pairs = make_pairs(llm, CHUNKS, SPLIT, 10)

    by_source = {p["source"]: p for p in pairs}
    assert sorted(by_source) == ["AIA-Art5-1@en", "AIA-Art5-1@fr", "AIA-Art9-1#1@en"]
    assert by_source["AIA-Art5-1@fr"]["positive"] == chunk("AIA-Art5-1", "fr").embed_text
    assert by_source["AIA-Art5-1@fr"]["lang"] == "fr"
    assert len(llm.calls) == 2


def test_make_pairs_screens_each_question():
    """A short or repeated question keeps its reasons, for the review to see."""
    llm = ScriptedLLM(reply("Who must keep the logs and for how long?", "Qui ?"))

    screens = {p["source"]: p["screen"] for p in make_pairs(llm, CHUNKS, SPLIT, 10)}

    assert screens["AIA-Art5-1@fr"] == "too short"
    assert sorted([screens["AIA-Art5-1@en"], screens["AIA-Art9-1#1@en"]]) == ["", "duplicate"]


def test_review_sample_is_seeded_and_bounded():
    """The same pairs give the same sample, never more pairs than there are."""
    pairs = [{"source": f"AIA-Art{i}-1@en"} for i in range(80)]

    assert review_sample(pairs, 50) == review_sample(pairs, 50)
    assert len(review_sample(pairs, 50)) == 50
    assert len(review_sample(pairs[:10], 50)) == 10
