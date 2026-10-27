from datetime import date

from actwise.api.guards import DailyCap


def test_daily_cap_resets_next_day():
    """The cap allows N requests, refuses the next one, and allows again after midnight."""
    today = date(2026, 10, 28)
    cap = DailyCap(2, today=lambda: today)  # reads `today` at each call

    first_day = [cap.allow() for _ in range(3)]
    today = date(2026, 10, 29)

    assert first_day == [True, True, False]
    assert cap.allow()
