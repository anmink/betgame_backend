# app/services/bet_service.py
from app.db.supabase_client import supabase
from app.models.bet import Bet
from fastapi import HTTPException

class BetService:
    @staticmethod
    async def get_bets(user_id: str):
        try:
            response = supabase.table("bets").select("*").eq("user_id", user_id).execute()
            return response.data
        except Exception as e:
            raise Exception(f"Error fetching bets: {e}")
    
    @staticmethod
    async def place_bet(bet: Bet, user_id: str):
        # 1. Nutzer abrufen
        response = supabase.table("users").select("*").eq("id", user_id).execute()
        user = response.data[0]
        balance = user["balance"]

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
        }).execute()

        return {"message": "Bet placed successfully"}
    
    @staticmethod
    async def delete_bet(bet_id: str, user_id: str, match_id: str):
        response_bet = supabase.table("bets").select("*").eq("id", bet_id).execute()
        bet = response_bet.data[0]
        bet_amount = bet["amount"]
        response_match = supabase.table("matches").select("*").eq("fixture_id", match_id).execute()
        match = response_match.data[0]
        match_status = match["fixture_status"]

        print(match_id)

        if match_status != "Not Started":
            raise HTTPException(status_code=400, detail="Game has already started or finished")
        response_user = supabase.table("users").select("*").eq("id", user_id).execute()
        user = response_user.data[0]
        user_balance = user["balance"]
        new_user_balance = user_balance + bet_amount

        supabase.table("users").update({"balance": new_user_balance}).eq("id", user_id).execute()
        supabase.table("bets").delete().eq("id", bet_id).execute()

        return {"message": "Bet deleted successfully"}


        
