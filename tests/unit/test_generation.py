from actwise.evaluation.generation import by_source, summarise_answers


def row(**fields):
    """An answer row with harmless defaults."""
    base = {
        "lang": "en",
        "source": "hand",
        "gold": ["AIA-Art5"],
        "answer": "Banned [AIA-Art5-1].",
        "refused": False,
        "reason": "",
        "citations": ["AIA-Art5-1"],
        "invented": [],
        "model": "m",
        "input_tokens": 10,
        "output_tokens": 5,
    }
    return base | fields


ROWS = [
    row(
        citations=["AIA-Art5-1", "AIA-Art3-1"],
        invented=["AIA-Art99-1"],
        judge={"score": 5, "reason": "", "unsupported": ["AIA-Art3-1"]},
    ),
    row(lang="fr", judge={"score": 3, "reason": "", "unsupported": []}),
    row(refused=True, reason="uncited", citations=[], answer="refusal"),  # in scope: false refusal
    row(gold=[], refused=True, reason="not_covered", citations=[], answer="refusal"),
    row(
        gold=[],
        citations=[],
        answer="An out-of-scope answer.",
        judge={"score": None, "reason": "?", "unsupported": []},
    ),
]


def test_refusal_and_false_refusal_rates():
    """Refusals count on out-of-scope questions; refusals of in-scope ones are false refusals."""
    s = summarise_answers(ROWS)

    assert (s["refusal_rate"], s["false_refusal_rate"]) == (0.5, round(1 / 3, 4))
    assert s["refusal_reasons"] == {"uncited": 1, "not_covered": 1}


def test_citation_precision_strict_and_lenient():
    """Strict: the cited article is gold (2 of 3). Lenient: the judge doesn't object (2 of 3)."""
    s = summarise_answers(ROWS)

    assert s["citation_precision_strict"] == round(2 / 3, 4)
    assert s["citation_precision_lenient"] == round(2 / 3, 4)


def test_faithfulness_and_judge_failures():
    """Faithfulness averages the readable verdicts; an unreadable one is counted apart."""
    s = summarise_answers(ROWS)

    assert s["faithfulness"] == (1.0 + 0.5) / 2
    assert s["fully_supported"] == 0.5  # one 5 and one 3
    assert (s["judged"], s["judge_failed"]) == (2, 1)
    assert s["invented_citations"] == 1 and s["invented_shown"] == 0


def test_an_invented_citation_left_in_an_answer_is_counted_as_shown():
    """The metric measures what users see; the pipeline's job is to keep it at 0."""
    assert summarise_answers([row(invented=["AIA-Art5-1"])])["invented_shown"] == 1


def test_no_judge_means_no_faithfulness():
    """Without verdicts, the judge-based numbers are None rather than 0."""
    s = summarise_answers([row()])

    assert s["faithfulness"] is None and s["citation_precision_lenient"] is None


def test_by_source():
    """Hand-written and synthetic questions are summarised apart."""
    rows = [
        row(),
        row(source="synthetic", refused=True, reason="uncited", citations=[], answer="r"),
    ]

    sources = by_source(rows)

    assert sources["hand"]["false_refusal_rate"] == 0.0
    assert sources["synthetic"]["false_refusal_rate"] == 1.0
