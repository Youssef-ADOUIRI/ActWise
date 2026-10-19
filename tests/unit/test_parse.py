from actwise.ingest.parse import normalise_lines, parse_regulation
from tests.unit.sample_text import EN_SAMPLE, FR_SAMPLE


def test_parse_structure():
    units = parse_regulation(EN_SAMPLE)

    assert [(u.kind, u.number) for u in units] == [
        ("recital", "1"),
        ("recital", "2"),
        ("article", "1"),
        ("article", "3"),
        ("article", "5"),
        ("annex", "III"),
    ]
    recital_2 = units[1].paragraphs[0].text
    assert recital_2 == "AI systems can be easily deployed in a large variety of sectors."
    article_1 = units[2]
    assert article_1.title == "Subject matter"
    assert "(a) harmonised rules" in article_1.paragraphs[1].text
    assert "(b) prohibitions" in article_1.paragraphs[1].text


def test_chapter_titles_not_glued():
    units = parse_regulation(EN_SAMPLE)
    texts = " ".join(p.text for u in units for p in u.paragraphs)

    assert "PROHIBITED AI PRACTICES" not in texts
    assert "CHAPTER" not in texts


def test_french_structure():
    units = parse_regulation(FR_SAMPLE)

    assert [(u.kind, u.number) for u in units] == [
        ("recital", "1"),
        ("recital", "2"),
        ("article", "1"),
        ("article", "3"),
        ("article", "5"),
        ("annex", "III"),
    ]
    definitions = units[3]
    assert [p.number for p in definitions.paragraphs] == [None, "1", "2"]


def test_footnote_marks_are_removed():
    lines = normalise_lines("opinion of the Committee\n(\n12\n)\n,\nand of the Council")

    assert lines == ["opinion of the Committee,", "and of the Council"]


def test_signatures_and_footnotes_after_body_are_ignored():
    text = """\
Article 113
Entry into force
This Regulation shall enter into force on the twentieth day.
This Regulation shall be binding in its entirety.
Done at Brussels, 13 June 2024.
For the European Parliament
(
1
)
OJ C 517, 22.12.2021, p. 56.
ANNEX I
List of Union harmonisation legislation
1. Directive 2006/42/EC on machinery.
"""
    article, annex = parse_regulation(text)

    assert article.paragraphs[0].text.endswith("on the twentieth day.")
    assert annex.paragraphs[0].text == "Directive 2006/42/EC on machinery."


def test_page_footer_is_ignored():
    text = "ANNEX XIII\nCriteria\n(g) the number of registered end-users.\n"
    text += "ELI: http://data.europa.eu/eli/reg/2024/1689/oj\nISSN 1977-0677 (electronic edition)\n"
    (annex,) = parse_regulation(text)

    assert annex.paragraphs[0].text == "(g) the number of registered end-users."


def test_annex_lettered_sections_restart_numbering():
    text = """\
ANNEX VIII
Information to be submitted upon registration
Section A — Information to be submitted by providers
1. The name of the provider;
2. The trade name of the system;
Section B — Information to be submitted by deployers
1. The name of the deployer;
"""
    (annex,) = parse_regulation(text)

    assert [p.number for p in annex.paragraphs] == ["a.0", "a.1", "a.2", "b.0", "b.1"]
    assert annex.paragraphs[3].text.startswith("Section B")


def test_annex_numbered_sections_keep_the_annex_open():
    text = """\
ANNEX XI
Technical documentation
Section 1
Information to be provided by all providers
1. A general description of the model;
Section 2
Additional information
1. A detailed description of the evaluation strategies;
"""
    (annex,) = parse_regulation(text)

    assert [p.number for p in annex.paragraphs] == ["1.0", "1.1", "2.0", "2.1"]
    assert annex.paragraphs[2].text == "Section 2 Additional information"


def test_gdpr_section_heading_is_skipped():
    text = """\
Article 11
Title
Text of 11.
Section 1
Transparency and modalities
Article 12
Title
Text.
"""
    article_11, _ = parse_regulation(text)

    assert article_11.paragraphs[0].text == "Text of 11."
