# app/services/bet_service.py
from app.db.supabase_client import supabase
from app.models.bet import Bet
from app.middleware.auth_dependency import get_current_user
from fastapi import HTTPException, Depends


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
    
    @staticmethod
    async def check_bet():
        try:
            user_id = "6de5b915-2c47-4d58-8266-eb1c610850d5"
            bets_response = supabase.table("bets").select("*").eq("user_id", user_id).execute()
            bets = bets_response.data

            users_response = supabase.table("users").select("*").eq("id", user_id).execute()
            user = users_response.data[0]

            if not bets:
                return {"message": "Not bets"}
            
            for bet in bets:
                matches_response = supabase.table("matches").select("*").eq("fixture_id", bet["match_id"]).execute()
                match = matches_response.data[0]
                if bet["check_status"] == None:
                    if match["fixture_status"] == "Match Finished":
                        """ print("check bet", bet["match_id"])
                        print("prediction was...", bet["prediction"])
                        print("result was...", match["teamhome_winner"], match["teamaway_winner"])
                        print("user amount before check", user["balance"]) """
                        if bet["prediction"] == "home" and match["teamhome_winner"] == True:
                            win_money = bet["amount"] * bet["odds"]
                            new_user_amount = win_money + user["balance"]
                            supabase.table("users").update({"balance": new_user_amount}).eq("id", user_id).execute()
                            supabase.table("bets").update({"check_status": True}).eq("match_id", bet["match_id"]).execute()
                        elif bet["prediction"] == "away" and match["teamaway_winner"] == True:
                            win_money = bet["amount"] * bet["odds"]
                            new_user_amount = win_money + user["balance"]
                            supabase.table("users").update({"balance": new_user_amount}).eq("id", user_id).execute()
                            supabase.table("bets").update({"check_status": True}).eq("match_id", bet["match_id"]).execute()
                        elif bet["prediction"] == "draw" and match["teamhome_winner"] == None and match["teamaway_winner"] == None:
                            win_money = bet["amount"] * bet["odds"]
                            new_user_amount = win_money + user["balance"]
                            supabase.table("users").update({"balance": new_user_amount}).eq("id", user_id).execute()
                            supabase.table("bets").update({"check_status": True}).eq("match_id", bet["match_id"]).execute()
                        else:
                            print("no win")
                            supabase.table("bets").update({"check_status": True}).eq("match_id", bet["match_id"]).execute()
                    else:
                        print("not started", bet["match_id"])
                    
                    
                    
                else:
                    print("bet has been checked before", bet["match_id"])




        except Exception as e:
            raise Exception(f"Error fetching bets: {e}")


        
