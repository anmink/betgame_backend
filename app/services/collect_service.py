from datetime import datetime

from app.core.game_config import COLLECT_COOLDOWN
from app.repositories.match_repository import MatchRepository
from app.repositories.user_repository import UserRepository
from app.schemas.collect import CollectResponse
from app.services.game_rules import cups_for_collect, is_matchday, next_collect_at


class CollectService:
    def __init__(self, users: UserRepository, matches: MatchRepository):
        self.users = users
        self.matches = matches

    def collect(self, user_id: str, now: datetime) -> CollectResponse:
        kickoffs = self.matches.kickoff_times_around(now)
        cups = cups_for_collect(is_matchday(now, kickoffs))
        becher = self.users.collect_cups(user_id, cups, now, COLLECT_COOLDOWN)
        return CollectResponse(collected=cups, becher=becher, next_collect_at=next_collect_at(now))
