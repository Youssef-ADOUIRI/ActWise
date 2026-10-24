from actwise.generation.citations import (
    extract_citations,
    invented_citations,
    strip_citations,
    uncited_sentences,
)
from actwise.ids import paragraph_id


def test_extract_citations():
    """A comma list in one bracket gives two ids; `[1]` and `[note]` give none."""
    answer = "High-risk systems are listed [AIA-AnnexIII-4, AIA-Art6-2]. See [1] and [note]."

    assert extract_citations(answer) == ["AIA-AnnexIII-4", "AIA-Art6-2"]


def test_extract_citations_keeps_first_use_order_without_duplicates():
    """An id cited twice is listed once, where it first appears."""
    answer = (
        "Fines apply [GDPR-Art83-5, GDPR-Art83-5]. Erasure [GDPR-Art17-1]. Fines [GDPR-Art83-5]."
    )

    assert extract_citations(answer) == ["GDPR-Art83-5", "GDPR-Art17-1"]


def test_citations_are_paragraph_level():
    """Citing part 2 of a long paragraph counts as citing the paragraph."""
    assert extract_citations("Purpose matters [AIA-Art3-12#2].") == ["AIA-Art3-12"]
    assert paragraph_id("AIA-Art3-12#2") == "AIA-Art3-12"


def test_verify_flags_invented():
    """A cited id that was not retrieved is invented; a sentence without a citation is counted."""
    answer = "Social scoring is banned [AIA-Art5-1]. Providers register [AIA-Art49-1]. That is all."

    assert invented_citations(answer, {"AIA-Art5-1", "AIA-Art9-1"}) == ["AIA-Art49-1"]
    assert uncited_sentences(answer) == 1


def test_strip_removes_only_the_exact_invented_id():
    """An invented AIA-Art6 next to a valid AIA-Art6-2 leaves the valid one intact (R2)."""
    answer = "It is high-risk [AIA-Art6, AIA-Art6-2]. It is also listed [AIA-Art6]."

    assert strip_citations(answer, {"AIA-Art6"}) == (
        "It is high-risk [AIA-Art6-2]. It is also listed."
    )


def test_strip_matches_the_paragraph_of_a_cited_part():
    """An invented paragraph is removed even when the model cites one of its parts."""
    assert strip_citations("Fines [GDPR-Art99-1#2].", {"GDPR-Art99-1"}) == "Fines."
