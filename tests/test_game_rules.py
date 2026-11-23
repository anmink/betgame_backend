from datetime import UTC, datetime

from app.core.game_config import CUPS_PER_COLLECT, CUPS_PER_COLLECT_MATCHDAY
from app.services.game_rules import cups_for_collect, is_matchday

KICKOFF = datetime(2026, 11, 21, 14, 30, tzinfo=UTC)


def utc(day: int, hour: int, minute: int = 0) -> datetime:
    return datetime(2026, 11, day, hour, minute, tzinfo=UTC)


def test_is_matchday_on_the_day_of_a_match():
    assert is_matchday(utc(21, 10), [KICKOFF])


def test_is_not_matchday_the_day_before():
    assert not is_matchday(utc(20, 12), [KICKOFF])


def test_matchday_starts_at_midnight_german_time():
    assert is_matchday(utc(20, 23, 30), [KICKOFF])


def test_no_matches_means_no_matchday():
    assert not is_matchday(utc(21, 10), [])


def test_more_cups_on_matchday():
    assert cups_for_collect(True) == CUPS_PER_COLLECT_MATCHDAY
    assert cups_for_collect(False) == CUPS_PER_COLLECT
