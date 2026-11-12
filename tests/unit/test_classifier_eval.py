from actwise.agent.classifier import ClassifyOutcome
from actwise.agent.schemas import TIERS, Classification
from actwise.evaluation.classifier_eval import FAILED, classify_scenarios, summarise_classifications
from actwise.evaluation.scenarios import Scenario
from actwise.llm.base import LLMResponse, ToolCall
from actwise.retrieval.passages import Passage, to_hit
from tests.unit.toys import ScriptedLLM


def row(gold, predicted, ambiguous=False, lang="en"):
    """A scored scenario row."""
    return {
        "id": "s",
        "lang": lang,
        "ambiguous": ambiguous,
        "gold": gold,
        "predicted": predicted,
        "steps": 2,
        "lookups": 1,
    }


def test_accuracy_counts_clear_scenarios_only():
    """Ambiguous scenarios are scored apart; a failed run counts as a miss."""
    rows = [
        row("prohibited", "prohibited"),
        row("high_risk", "minimal_risk"),
        row("minimal_risk", "minimal_risk", ambiguous=True),
        {"id": "s", "lang": "fr", "ambiguous": False, "gold": "high_risk", "predicted": FAILED},
    ]

    s = summarise_classifications(rows)

    assert (s["clear"], s["accuracy"], s["accuracy_ambiguous"]) == (3, round(1 / 3, 4), 1.0)
    assert (s["failed"], s["dangerous_downgrades"], s["prohibited_as_minimal"]) == (1, 1, 0)
    assert s["by_lang"] == {"en": 0.5, "fr": 0.0}


def test_confusion_is_five_by_five_over_every_scenario_that_ran():
    """Every tier is a row and a column, zeros included; ambiguous runs count, failed ones don't."""
    rows = [
        row("prohibited", "high_risk"),
        row("minimal_risk", "minimal_risk", ambiguous=True),
        {"id": "s", "lang": "en", "ambiguous": False, "gold": "high_risk", "predicted": FAILED},
    ]

    confusion = summarise_classifications(rows)["confusion"]

    assert list(confusion) == list(TIERS)
    assert all(list(predicted) == list(TIERS) for predicted in confusion.values())
    assert confusion["prohibited"]["high_risk"] == 1
    assert confusion["minimal_risk"]["minimal_risk"] == 1
    assert sum(n for predicted in confusion.values() for n in predicted.values()) == 2


def test_recall_on_the_costly_tiers_counts_failed_runs_as_misses():
    """Recall on prohibited and high risk, over clear and ambiguous scenarios alike."""
    rows = [
        row("prohibited", "prohibited"),
        row("prohibited", "high_risk"),
        row("high_risk", "high_risk", ambiguous=True),
        {"id": "s", "lang": "en", "ambiguous": False, "gold": "high_risk", "predicted": FAILED},
        row("minimal_risk", "high_risk"),
    ]

    s = summarise_classifications(rows)

    assert (s["recall_prohibited"], s["recall_high_risk"]) == (0.5, 0.5)
    no_costly = summarise_classifications([row("minimal_risk", "minimal_risk")])
    assert no_costly["recall_high_risk"] is None


def test_prohibited_labelled_minimal_is_counted():
    """The worst error has its own counter."""
    assert (
        summarise_classifications([row("prohibited", "minimal_risk")])["prohibited_as_minimal"] == 1
    )


def test_classify_scenarios_records_failures_and_results():
    """A run that hits the step budget becomes a failed row; a good run records its result."""
    passage = to_hit(Passage("AIA-Art5-1", "en", "The following AI practices..."), 1.0)
    calls = [
        ToolCall("a", "search_ai_act", {"query": "social scoring"}),
        ToolCall(
            "b",
            "submit_classification",
            {"tier": "prohibited", "reasons": ["r"], "citations": ["AIA-Art5-1"], "confidence": 1},
        ),
    ]
    good = ScriptedLLM(LLMResponse("", calls[:1], 1, 1, "m"), LLMResponse("", calls[1:], 1, 1, "m"))
    stuck = ScriptedLLM(LLMResponse("I won't use tools.", [], 1, 1, "m"))
    scenario = Scenario(
        "s01", "dev", "en", False, "prohibited", "AIA-Art5-1", "", "Scoring.", "yes"
    )

    [ok] = classify_scenarios(good, lambda q, k: [passage], {}, [scenario])
    [failed] = classify_scenarios(stuck, lambda q, k: [passage], {}, [scenario])

    assert (ok["predicted"], ok["citations"], ok["steps"]) == ("prohibited", ["AIA-Art5-1"], 2)
    assert "tier" not in ok  # stored once, as `predicted`
    assert failed["predicted"] == FAILED and "step" in failed["error"]


def test_classify_scenarios_runs_the_classifier_it_is_given():
    """Another classifier (the LangGraph one) goes through the same harness; cost is recorded."""
    seen = []

    def classifier(llm, search, articles, description):
        """Answers high risk after one model call that cost 100 + 20 tokens."""
        seen.append(description)
        llm.chat([{"role": "user", "content": description}])
        result = Classification(
            tier="high_risk", reasons=["r"], citations=["AIA-Art6-2"], confidence=0.5
        )
        return ClassifyOutcome(result, steps=1, lookups=3)

    scenario = Scenario("s02", "dev", "en", False, "high_risk", "AIA-Art6", "", "CVs.", "yes")
    llm = ScriptedLLM(LLMResponse("", [], 100, 20, "m"))

    [r] = classify_scenarios(llm, lambda q, k: [], {}, [scenario], classifier)

    assert seen == ["CVs."]
    assert (r["predicted"], r["steps"], r["lookups"]) == ("high_risk", 1, 3)
    assert (r["input_tokens"], r["output_tokens"]) == (100, 20)
    assert r["seconds"] >= 0
