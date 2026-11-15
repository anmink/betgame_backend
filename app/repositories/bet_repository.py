from postgrest.exceptions import APIError
from supabase import Client

from app.core.errors import InsufficientCoinsError
from app.db.supabase_client import supabase


class BetRepository:
    def __init__(self, client: Client = supabase):
        self.client = client

    def list_for_user(self, user_id: str) -> list[dict]:
        result = self.client.table("bets").select("*, matches(*)").eq("user_id", user_id).execute()
        return result.data

    def get_by_id(self, bet_id: int) -> dict | None:
        result = self.client.table("bets").select("*").eq("id", bet_id).maybe_single().execute()
        return result.data if result else None

    def list_open(self) -> list[dict]:
        result = self.client.table("bets").select("*").eq("status", "open").execute()
        return result.data

    def place(self, user_id: str, match_id: int, stake: int, prediction: str, odds: float) -> int:
        try:
            result = self.client.rpc(
                "place_bet",
                {
                    "p_user_id": user_id,
                    "p_match_id": match_id,
                    "p_stake": stake,
                    "p_prediction": prediction,
                    "p_odds": odds,
                },
            ).execute()
        except APIError as e:
            if "insufficient_coins" in (e.message or ""):
                raise InsufficientCoinsError("Not enough coins") from e
            raise
        return result.data
