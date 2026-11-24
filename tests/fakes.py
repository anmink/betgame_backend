from app.core.errors import CooldownActiveError
from app.core.game_config import START_COINS


class FakeUserRepository:
    def __init__(self, users: dict | None = None):
        self.users = users or {}

    def get_by_id(self, user_id: str) -> dict | None:
        return self.users.get(user_id)

    def create(self, user_id: str, username: str) -> dict:
        user = {"id": user_id, "username": username, "coins": START_COINS, "becher": 0}
        self.users[user_id] = user
        return user

    def collect_cups(self, user_id, cups, now, cooldown):
        user = self.users[user_id]
        last = user.get("last_collect_at")
        if last is not None and now < last + cooldown:
            raise CooldownActiveError("You can collect again later")
        user["becher"] = user.get("becher", 0) + cups
        user["last_collect_at"] = now
        return user["becher"]


class FakeMatchRepository:
    def __init__(self, kickoffs=None):
        self.kickoffs = kickoffs or []

    def kickoff_times_around(self, now):
        return self.kickoffs
