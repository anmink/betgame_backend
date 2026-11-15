import math
from datetime import datetime
from decimal import Decimal

from app.core.errors import BettingClosedError

ODDS_FIELDS = {"home": "odd_home", "draw": "odd_draw", "away": "odd_away"}


def is_betting_open(match: dict, now: datetime) -> bool:
    kickoff = datetime.fromisoformat(match["fixture_date"])
    return match["fixture_status"] == "Not Started" and now < kickoff


def odds_for(match: dict, prediction: str) -> float:
    odds = match[ODDS_FIELDS[prediction]]
    if odds is None:
        raise BettingClosedError("No odds available for this match")
    return odds


def is_winning(prediction: str, goals_home: int, goals_away: int) -> bool:
    if goals_home > goals_away:
        result = "home"
    elif goals_home < goals_away:
        result = "away"
    else:
        result = "draw"
    return prediction == result


def calculate_payout(stake: int, odds: float) -> int:
    return math.floor(Decimal(str(odds)) * stake)
