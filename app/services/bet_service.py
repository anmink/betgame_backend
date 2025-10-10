# app/services/bet_service.py
from app.db.supabase_client import supabase
from app.models.bet import BetModel
from fastapi import HTTPException

class BetService:
    @staticmethod
    async def get_bets(user_id: str):
        response = supabase.table("bets").select("*").eq("user_id", user_id).execute()
        if response.error:
            raise HTTPException(status_code=500, detail="Error fetching bets")
        return response.data
    
    @staticmethod
    async def place_bet(bet: BetModel, user_id: str):
        # 1. Nutzer abrufen
        user = supabase.table("users").select("*").eq("id", user_id).single().execute()
        balance = user.data["balance"]

        # 2. Prüfen, ob genug Guthaben vorhanden ist
        if balance < bet.amount:
            raise HTTPException(status_code=400, detail="Not enough balance")

        # 3. Einsatz abziehen und Wette speichern
        supabase.table("users").update({"balance": balance - bet.amount}).eq("id", user_id).execute()
        supabase.table("bets").insert({
            "user_id": user_id,
            "match_id": bet.match_id,
            "amount": bet.amount,
            "odds": bet.odds,
            "prediction": bet.prediction,
            "status": "open"
        }).execute()

        return {"message": "Bet placed successfully"}
    
    @staticmethod
    async def delete_bet(bet_id: str, user_id: str):
        bet = supabase.table("bets").select("*").eq("id", bet_id).single().execute()
        if bet.data["status"] != "open":
            raise HTTPException(status_code=400, detail="Bet already closed")

        # Einsatz zurückzahlen
        user = supabase.table("users").select("*").eq("id", user_id).single().execute()
        balance = user.data["balance"] + bet.data["amount"]

        supabase.table("users").update({"balance": balance}).eq("id", user_id).execute()
        supabase.table("bets").delete().eq("id", bet_id).execute()

        return {"message": "Bet deleted successfully"}


        
