"""The Google Sheets "AI system register": one row per classification, never the description.

The API logs each /classify and /upload result here when GSHEETS_SA_JSON is set
(docs/integrations.md, decision 014). A description is identified by a keyed hash
(HMAC-SHA-256 with REGISTER_KEY): equal descriptions share a row id, and whoever reads
the sheet cannot check a guessed description without the key.
"""

from __future__ import annotations

import hashlib
import hmac
import json
from collections.abc import Callable, Mapping
from datetime import UTC, datetime
from functools import cached_property
from typing import Any

from actwise.agent.classifier import ClassifyOutcome

HEADER = ["timestamp", "description_hmac", "tier", "confidence", "citations", "model"]
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]  # the sheets shared with it; no Drive
TIMEOUT = 5.0  # seconds: a slow Sheets call must not use up the request's model budget


def register_row(
    description: str, outcome: ClassifyOutcome, key: bytes, now: datetime | None = None
) -> list[str]:
    """Timestamp, the description's keyed hash (12 hex), tier, confidence, citations, model."""
    digest = hmac.new(key, description.encode("utf-8"), hashlib.sha256).hexdigest()[:12]
    result = outcome.result
    return [
        (now or datetime.now(UTC)).isoformat(timespec="seconds"),
        digest,
        result.tier,
        f"{result.confidence:.2f}",
        ", ".join(result.citations),
        outcome.model,
    ]


class SheetsRegister:
    """Appends one row per classification to a worksheet, opened on the first one."""

    def __init__(self, open_sheet: Callable[[], Any], key: bytes):
        """`open_sheet` returns the worksheet: a Sheets outage at start-up can't stop the API."""
        self.open_sheet, self.key = open_sheet, key

    @cached_property
    def sheet(self) -> Any:
        """The worksheet; an empty one gets the column names first."""
        sheet = self.open_sheet()
        if not sheet.row_values(1):
            sheet.append_row(HEADER, value_input_option="RAW")
        return sheet

    def log(self, description: str, outcome: ClassifyOutcome) -> None:
        """Append the row, stored as typed (RAW): a cell starting with '=' stays text."""
        row = register_row(description, outcome, self.key)
        self.sheet.append_row(row, value_input_option="RAW")

    @classmethod
    def from_env(cls, env: Mapping[str, str]) -> SheetsRegister | None:
        """GSHEETS_SA_JSON (the service account key), GSHEETS_REGISTER_ID, REGISTER_KEY.

        None without GSHEETS_SA_JSON: the register is off.
        """
        if not env.get("GSHEETS_SA_JSON"):
            return None
        import gspread

        client = gspread.service_account_from_dict(
            json.loads(env["GSHEETS_SA_JSON"]), scopes=SCOPES
        )
        client.set_timeout(TIMEOUT)
        sheet_id = env["GSHEETS_REGISTER_ID"]
        return cls(lambda: client.open_by_key(sheet_id).sheet1, env["REGISTER_KEY"].encode())
