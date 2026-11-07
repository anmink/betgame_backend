from supabase import Client

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
