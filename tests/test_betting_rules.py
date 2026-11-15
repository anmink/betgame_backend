from datetime import UTC, datetime

import pytest

from app.core.errors import BettingClosedError
from app.services.betting_rules import is_betting_open, odds_for, is_winning, calculate_payout

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


@pytest.mark.parametrize(
    ("prediction", "goals_home", "goals_away", "expected"),
    [
        ("home", 2, 1, True),
        ("home", 1, 1, False),
        ("home", 0, 1, False),
        ("draw", 1, 1, True),
        ("away", 0, 1, True),
        ("away", 2, 1, False),
    ],
)
def test_is_winning(prediction, goals_home, goals_away, expected):
    assert is_winning(prediction, goals_home, goals_away) is expected


@pytest.mark.parametrize(
    ("stake", "odds", "expected"),
    [(10, 2.0, 20), (10, 1.85, 18), (1, 1.5, 1), (100, 1.13, 113)],
)
def test_calculate_payout(stake, odds, expected):
    assert calculate_payout(stake, odds) == expected
