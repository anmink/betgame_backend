from datetime import datetime

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
