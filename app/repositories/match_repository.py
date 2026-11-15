from supabase import Client

from app.db.supabase_client import supabase


class MatchRepository:
    def __init__(self, client: Client = supabase):
        self.client = client

    def get_by_id(self, fixture_id: int) -> dict | None:
        result = (
            self.client.table("matches")
            .select("*")
            .eq("fixture_id", fixture_id)
            .maybe_single()
            .execute()
        )
        return result.data if result else None
