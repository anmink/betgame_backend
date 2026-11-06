from app.db.supabase_client import supabase


class UserService:
    async def get_user(user_id: str):
        try:
            response = supabase.table("users").select("*").eq("id", user_id).single().execute().data
            return response
        except Exception as e:
            raise Exception(f"Error fetching bets: {e}") from e
