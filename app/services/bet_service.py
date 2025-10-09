# app/services/bet_service.py
from app.db.supabase_client import supabase

class BetService:
    @staticmethod
    def place_bet(user_id: int, match_id: int, amount: float, odds: float):
        # 1. User abrufen
        response = supabase.table("users").select("*").eq("id", user_id).single().execute()
        user = response.data

        if not user:
            raise ValueError("User not found")

        balance = user["balance"]

        # 2. Balance prüfen
        if balance < amount:
            raise ValueError("Insufficient balance")

        new_balance = balance - amount

        # 3. Wette einfügen
        bet_data = {
            "user_id": user_id,
            "match_id": match_id,
            "amount": amount,
            "odds": odds
        }
        supabase.table("bets").insert(bet_data).execute()

        # 4. Balance aktualisieren
        supabase.table("users").update({"balance": new_balance}).eq("id", user_id).execute()

        # 5. Rückgabe
        return {**bet_data, "new_balance": new_balance}
