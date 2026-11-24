from datetime import datetime
from zoneinfo import ZoneInfo

from app.core.game_config import COLLECT_COOLDOWN, CUPS_PER_COLLECT, CUPS_PER_COLLECT_MATCHDAY

BERLIN = ZoneInfo("Europe/Berlin")


def is_matchday(now: datetime, kickoff_times: list[datetime]) -> bool:
    today = now.astimezone(BERLIN).date()
    return any(kickoff.astimezone(BERLIN).date() == today for kickoff in kickoff_times)


def cups_for_collect(matchday: bool) -> int:
    return CUPS_PER_COLLECT_MATCHDAY if matchday else CUPS_PER_COLLECT


def next_collect_at(collect_at: datetime) -> datetime:
    return collect_at + COLLECT_COOLDOWN
