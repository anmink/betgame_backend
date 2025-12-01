from app.db.supabase_client import supabase
from app.models.bet import Bet
from fastapi import HTTPException


class UserService:
    async def get_bets(user_id: str):
        try:
            response = (
                supabase.table("users")
                .select("*")
                .eq("id", user_id)
                .single()
                .execute()
                .data
            )
            return response
        except Exception as e:
            raise Exception(f"Error fetching bets: {e}")
