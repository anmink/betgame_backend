from datetime import datetime, timedelta

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

    def kickoff_times_around(self, now: datetime) -> list[datetime]:
        start = (now - timedelta(days=1)).isoformat()
        end = (now + timedelta(days=1)).isoformat()
        result = (
            self.client.table("matches")
            .select("fixture_date")
            .gte("fixture_date", start)
            .lte("fixture_date", end)
            .execute()
        )
        return [datetime.fromisoformat(row["fixture_date"]) for row in result.data]
