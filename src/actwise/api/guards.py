"""Cost guardrails for a public demo: a daily request cap that traffic cannot get around."""

from __future__ import annotations

import threading
from collections.abc import Callable
from datetime import date


class DailyCap:
    """At most `limit` requests a day, counted in memory by each instance (decision 009)."""

    def __init__(self, limit: int, today: Callable[[], date] = date.today):
        """`today` is injected, so a test can move to the next day."""
        self.limit, self.today = limit, today
        self._day, self._count = today(), 0
        self._lock = threading.Lock()  # FastAPI runs sync routes in a thread pool

    def allow(self) -> bool:
        """Count one request, or return False once today's limit is reached."""
        with self._lock:
            if (day := self.today()) != self._day:
                self._day, self._count = day, 0
            if self._count >= self.limit:
                return False
            self._count += 1
            return True
