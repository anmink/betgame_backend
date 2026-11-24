from datetime import datetime, timedelta

from postgrest.exceptions import APIError
from supabase import Client

from app.core.errors import CooldownActiveError
from app.core.game_config import START_COINS
from app.db.supabase_client import supabase


class UserRepository:
    def __init__(self, client: Client = supabase):
        self.client = client

    def get_by_id(self, user_id: str) -> dict | None:
        result = self.client.table("users").select("*").eq("id", user_id).maybe_single().execute()
        return result.data if result else None

    def create(self, user_id: str, username: str) -> dict:
        result = (
            self.client.table("users")
            .insert({"id": user_id, "username": username, "coins": START_COINS})
            .execute()
        )
        return result.data[0]

    def collect_cups(self, user_id: str, cups: int, now: datetime, cooldown: timedelta) -> int:
        try:
            result = self.client.rpc(
                "collect_cups",
                {
                    "p_user_id": user_id,
                    "p_cups": cups,
                    "p_now": now.isoformat(),
                    "p_cooldown": f"{int(cooldown.total_seconds())} seconds",
                },
            ).execute()
        except APIError as e:
            if "cooldown_active" in (e.message or ""):
                raise CooldownActiveError("You can collect again later") from e
            raise
        return int(result.data)
