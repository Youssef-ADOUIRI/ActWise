"""Turn the plain text of an EUR-Lex regulation into recitals, articles and annexes.

The parser reads text lines, not CSS classes, so it survives markup changes.
Always check the counts: the AI Act has 180 recitals, 113 articles and 13 annexes;
the GDPR has 173 recitals and 99 articles.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

ARTICLE = re.compile(r"^Article (\d+|premier)$")
ANNEX = re.compile(r"^ANNEXE? ([IVXL]+)$")
STRUCTURE = re.compile(r"^(?:CHAPTER|CHAPITRE|SECTION|Section|TITLE|TITRE) ([IVXL\d]+)$")
PARAGRAPH = re.compile(r"^(\d+)\. (.*)$")  # "1. text"
NUMBERED_POINT = re.compile(r"^\(?(\d+)\) (.*)$")  # "(1) text" in EN, "1) text" in FR
ANNEX_SECTION = re.compile(r"^Section ([A-Z])(?:\.| —| -) ")  # "Section B — Information ..."
LONE_MARKER = re.compile(r"^(?:\(\d+\)|\d+\)|\d+\.)$")  # "(1)", "1)" or "1." alone on a line
PREAMBLE_END = re.compile(r"^(?:HAVE ADOPTED THIS REGULATION|ONT ADOPTÉ LE PRÉSENT RÈGLEMENT)")
BODY_END = re.compile(  # signatures, footnotes or the page footer follow these lines
    r"^(?:Done at|Fait à|This Regulation shall be binding|Le présent règlement est obligatoire"
    r"|ELI: http)"
)


@dataclass
class Paragraph:
    number: str | None
    text: str


@dataclass
class Unit:
    kind: str  # "recital" | "article" | "annex"
    number: str  # "63", "6", "III"
    title: str = ""
    paragraphs: list[Paragraph] = field(default_factory=list)
    style: str | None = None  # "para" for "1." paragraphs, "def" for "(1)" definitions
    section: str = ""  # "b" or "2" inside annexes split into sections

    def start_section(self, label: str, heading: str) -> None:
        """Annexes VIII and XI restart numbering in each section: points become b.1, 2.1..."""
        self.section = label.lower()
        self.paragraphs.append(Paragraph(f"{self.section}.0", heading))

    def add_line(self, line: str) -> None:
        """Start a new paragraph on '1.' or '(1)', otherwise continue the last one."""
        if self.kind == "annex" and (match := ANNEX_SECTION.match(line)):
            self.start_section(match[1], line)
        elif (match := PARAGRAPH.match(line)) and self.style in (None, "para"):
            self.style = "para"
            number = f"{self.section}.{match[1]}" if self.section else match[1]
            self.paragraphs.append(Paragraph(number, match[2]))
        elif (
            (match := NUMBERED_POINT.match(line))
            and self.kind == "article"
            and self.style in (None, "def")
        ):
            self.style = "def"
            self.paragraphs.append(Paragraph(match[1], match[2]))
        elif self.paragraphs:
            self.paragraphs[-1].text += " " + line
        else:
            self.paragraphs.append(Paragraph(None, line))


def normalise_lines(text: str) -> list[str]:
    """Collapse whitespace, drop blank lines and footnote marks, glue lone markers."""
    lines = [" ".join(line.split()) for line in text.splitlines()]
    lines = [line for line in lines if line]
    return _glue_lone_markers(_drop_footnote_marks(lines))


def _is_punctuation(line: str) -> bool:
    return all(ch in ",.;:)" for ch in line)


def _drop_footnote_marks(lines: list[str]) -> list[str]:
    """EUR-Lex splits a footnote mark over lines: '(', '12', ')' and maybe ','."""
    out: list[str] = []
    i = 0
    while i < len(lines):
        is_mark = (
            lines[i] == "("
            and i + 2 < len(lines)
            and lines[i + 1].isdigit()
            and lines[i + 2].startswith(")")
        )
        if not is_mark:
            out.append(lines[i])
            i += 1
            continue

        rest = lines[i + 2][1:].strip()  # text after ")" on the same line
        i += 3
        if not rest and i < len(lines) and _is_punctuation(lines[i]):
            rest = lines[i]  # the "," that followed the mark on its own line
            i += 1
        if rest and out:
            out[-1] += rest if _is_punctuation(rest[0]) else " " + rest
    return out


def _glue_lone_markers(lines: list[str]) -> list[str]:
    """'(1)' alone on a line belongs to the next line: '(1)', 'text' -> '(1) text'."""
    out: list[str] = []
    i = 0
    while i < len(lines):
        if LONE_MARKER.match(lines[i]) and i + 1 < len(lines):
            out.append(f"{lines[i]} {lines[i + 1]}")
            i += 2
        else:
            out.append(lines[i])
            i += 1
    return out


def _line_after(lines: list[str], i: int) -> str:
    return lines[i + 1] if i + 1 < len(lines) else ""


def parse_regulation(text: str) -> list[Unit]:
    lines = normalise_lines(text)
    in_preamble = any(PREAMBLE_END.match(line) for line in lines)
    units: list[Unit] = []
    current: Unit | None = None
    i = 0

    while i < len(lines):
        line = lines[i]

        if in_preamble:
            if PREAMBLE_END.match(line):
                in_preamble, current = False, None
            elif match := NUMBERED_POINT.match(line):  # "(12) text" starts recital 12
                current = Unit("recital", match[1], paragraphs=[Paragraph(None, match[2])])
                units.append(current)
            elif current is not None:
                current.paragraphs[0].text += " " + line
            i += 1
            continue

        if BODY_END.match(line):  # signatures and footnotes follow; skip until next heading
            current = None
            i += 1
        elif match := STRUCTURE.match(line):  # a heading and its title line
            if current is not None and current.kind == "annex":
                current.start_section(match[1], f"{line} {_line_after(lines, i)}")
            else:
                current = None  # "CHAPTER II" closes the previous article
            i += 2
        elif match := ARTICLE.match(line):
            number = "1" if match[1] == "premier" else match[1]
            current = Unit("article", number, title=_line_after(lines, i))
            units.append(current)
            i += 2
        elif match := ANNEX.match(line):
            current = Unit("annex", match[1], title=_line_after(lines, i))
            units.append(current)
            i += 2
        else:
            if current is not None:
                current.add_line(line)
            i += 1

    return units
