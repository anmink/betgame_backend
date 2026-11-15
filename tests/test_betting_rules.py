from datetime import UTC, datetime

import pytest

from app.core.errors import BettingClosedError
from app.services.betting_rules import is_betting_open, odds_for

MATCH = {
    "fixture_status": "Not Started",
    "fixture_date": "2026-11-21T14:30:00+00:00",
    "odd_home": 1.85,
    "odd_draw": 3.40,
    "odd_away": None,
}


def at(hour: int, minute: int) -> datetime:
    return datetime(2026, 11, 21, hour, minute, tzinfo=UTC)


def test_betting_is_open_before_kickoff():
    assert is_betting_open(MATCH, at(14, 0))


def test_betting_is_closed_after_kickoff():
    assert not is_betting_open(MATCH, at(14, 31))


def test_betting_is_closed_when_match_has_started():
    started = {**MATCH, "fixture_status": "First Half, Kick Off"}
    assert not is_betting_open(started, at(14, 0))


def test_odds_come_from_the_match():
    assert odds_for(MATCH, "home") == 1.85


def test_missing_odds_close_betting():
    with pytest.raises(BettingClosedError):
        odds_for(MATCH, "away")
