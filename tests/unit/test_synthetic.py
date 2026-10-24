import pytest

from actwise.evaluation.synthetic import (
    draft_in_scope,
    draft_out_of_scope,
    normalise,
    pick_chunks,
    screen,
)
from actwise.ingest.chunk import Chunk
from actwise.llm.base import LLMResponse
from tests.unit.toys import ScriptedLLM


def chunk(cid, lang="en", kind="article", words=30):
    """A toy chunk of `words` words."""
    return Chunk(cid, "ai_act", lang, kind, "5", "1", "", " ".join(["mot"] * words))


IDS = ["AIA-Art5-1", "AIA-Art5-2", "AIA-Art9-1", "AIA-Art7-1"]
CHUNKS = [chunk(i, lang) for i in IDS for lang in ("en", "fr")]
CHUNKS += [chunk("AIA-Rec10", kind="recital"), chunk("AIA-Art11-1", words=10)]
SPLIT = {
    "AIA-Art5": "dev",
    "AIA-Art9": "dev",
    "AIA-Art7": "test",
    "AIA-Rec10": "dev",
    "AIA-Art11": "dev",
}


def test_pick_chunks_spreads_over_articles_first():
    """Two picks from dev come from two articles; no recital, short or test paragraph."""
    picked = pick_chunks(CHUNKS, SPLIT, "dev", 2)

    assert sorted(c.id.split("-")[1] for c in picked) == ["Art5", "Art9"]
    assert {c.lang for c in pick_chunks(CHUNKS, SPLIT, "dev", 3)} <= {"en", "fr"}
    assert {c.id for c in pick_chunks(CHUNKS, SPLIT, "dev", 10)} == {
        "AIA-Art5-1",
        "AIA-Art5-2",
        "AIA-Art9-1",
    }


def test_pick_chunks_is_seeded():
    """The same call draws the same paragraphs in the same languages."""
    assert pick_chunks(CHUNKS, SPLIT, "dev", 3) == pick_chunks(CHUNKS, SPLIT, "dev", 3)


@pytest.mark.parametrize(
    ("question", "kind", "reason"),
    [
        ("What does Article 6 require from providers?", "lookup", "names its article"),
        ("Who must keep the logs of a system?", "lookup", "duplicate"),
        ("Who registers?", "lookup", "too short"),
        ("Who must notify the authority in time?", "story", "unknown type 'story'"),
        ("", "lookup", "unreadable reply"),
    ],
)
def test_screen(question, kind, reason):
    """Each rule gives its reason; a question already seen is a duplicate."""
    seen = {normalise("Who must keep the logs of a system ?")}

    assert reason in screen({"question": question, "type": kind, "gold": ["AIA-Art12"]}, seen)


def test_a_good_candidate_passes_the_screen():
    """A fresh, specific question has no reason against it."""
    candidate = {
        "question": "Who must keep automatically generated logs?",
        "type": "obligation",
        "gold": ["AIA-Art19"],
    }

    assert screen(candidate, set()) == []


def test_draft_in_scope_writes_in_the_chunk_language():
    """The model gets the passage and the language; gold is the passage's article."""
    llm = ScriptedLLM(
        LLMResponse('{"question": "Q ?", "reference": "R.", "type": "lookup"}', [], 1, 1, "m")
    )

    draft = draft_in_scope(llm, chunk("AIA-Art5-2", "fr"), "dev")

    assert "Language: French" in llm.calls[0]["messages"][1]["content"]
    assert draft == {
        "lang": "fr",
        "type": "lookup",
        "question": "Q ?",
        "gold": ["AIA-Art5"],
        "reference": "R.",
        "split": "dev",
        "source": "AIA-Art5-2",
    }


def test_draft_out_of_scope_has_no_gold():
    """An out-of-scope draft is a not_covered question on its topic, with empty gold."""
    llm = ScriptedLLM(LLMResponse('{"question": "Q?", "reference": "R."}', [], 1, 1, "m"))

    draft = draft_out_of_scope(llm, "roaming charges", "en", "test")

    assert (draft["type"], draft["gold"], draft["source"], draft["split"]) == (
        "not_covered",
        [],
        "roaming charges",
        "test",
    )
