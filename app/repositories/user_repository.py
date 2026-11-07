from supabase import Client

from app.db.supabase_client import supabase


class UserRepository:
    def __init__(self, client: Client = supabase):
        self.client = client

    def get_by_id(self, user_id: str) -> dict | None:
        result = self.client.table("users").select("*").eq("id", user_id).maybe_single().execute()
        return result.data if result else None

    def create(self, user_id: str, username: str) -> dict:
        result = self.client.table("users").insert({"id": user_id, "username": username}).execute()
        return result.data[0]
