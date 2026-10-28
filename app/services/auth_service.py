from app.db.supabase_client import supabase


class AuthService:
    @staticmethod
    async def register_user(id: str, email: str):
        supabase.table("users").insert(
            {"id":  id, "username": email, "balance": 100}
        ).execute()
        return {"message": "User successfully registered"}
