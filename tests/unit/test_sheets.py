from datetime import UTC, datetime

from actwise.agent.schemas import Classification
from actwise.integrations.sheets import HEADER, SheetsRegister, register_row

DESCRIPTION = "A tool that ranks job applicants from their CVs."
RESULT = Classification(
    tier="high_risk",
    reasons=["It ranks applicants."],
    citations=["AIA-Art6-2", "AIA-AnnexIII-4"],
    confidence=0.8,
)
KEY = b"register-key"


class FakeSheet:
    """A worksheet in memory: rows appended with their input option."""

    def __init__(self, rows=None):
        """Start with `rows`."""
        self.rows, self.options = list(rows or []), []

    def row_values(self, number):
        """Row `number` (1-based), or [] past the end."""
        return self.rows[number - 1] if number <= len(self.rows) else []

    def append_row(self, values, value_input_option):
        """Add a row."""
        self.rows.append(values)
        self.options.append(value_input_option)


def test_register_row():
    """Timestamp, a 12-character keyed hash, tier, confidence to 2 places, citations, model."""
    now = datetime(2026, 11, 16, 9, 30, tzinfo=UTC)

    row = register_row(DESCRIPTION, RESULT, "gemini-test", KEY, now)

    assert row[0] == "2026-11-16T09:30:00+00:00"
    assert len(row[1]) == 12 and int(row[1], 16) >= 0
    assert row[2:] == ["high_risk", "0.80", "AIA-Art6-2, AIA-AnnexIII-4", "gemini-test"]
    assert len(row) == len(HEADER)
    assert not any("CV" in cell for cell in row)  # the description is never stored


def test_the_hash_needs_the_key():
    """The same description gives the same hash under one key, another under another key."""
    hashes = [register_row(DESCRIPTION, RESULT, "m", key)[1] for key in (KEY, KEY, b"other")]

    assert hashes[0] == hashes[1] != hashes[2]


def test_register_appends_raw_rows_and_writes_the_header_once():
    """An empty sheet gets the column names first; values are stored as typed (RAW)."""
    sheet = FakeSheet()
    opened = []
    register = SheetsRegister(lambda: opened.append(1) or sheet, KEY)

    register.log(DESCRIPTION, RESULT, "gemini-test")
    register.log(DESCRIPTION, RESULT, "gemini-test")

    assert sheet.rows[0] == HEADER and len(sheet.rows) == 3
    assert set(sheet.options) == {"RAW"} and opened == [1]


def test_register_keeps_an_existing_header():
    """A sheet that already has its header row gets only the new row."""
    sheet = FakeSheet([HEADER])

    SheetsRegister(lambda: sheet, KEY).log(DESCRIPTION, RESULT, "gemini-test")

    assert len(sheet.rows) == 2 and sheet.rows[1][2] == "high_risk"
