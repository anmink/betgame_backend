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
