# app/services/bet_service.py
from app.db.supabase_client import supabase
from app.models.bet import Bet
from fastapi import HTTPException


class BetService:
    @staticmethod
    async def get_bets(user_id: str):
        try:
            response = (
                supabase.from_("bets")
                .select(
                    """
                    id,
                    amount,
                    prediction,
                    odds,
                    match_id,
                    status,
                    matches (
                        fixture_id,
                        fixture_date,
                        fixture_status,
                        league_name,
                        teamhome_name,
                        teamhome_logo,
                        teamaway_name,
                        teamaway_logo,
                        goal_home,
                        goal_away
                    )
                """
                )
                .eq("user_id", user_id)
                .execute()
            )

            # Sortiere: Jüngstes Datum zuerst (reverse=True)
            sorted_bets = sorted(
                response.data,
                key=lambda bet: (
                    bet["matches"]["fixture_date"] if bet.get("matches") else ""
                ),
                reverse=True,  # Neueste/Jüngste Datum zuerst
            )

            return sorted_bets

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
        supabase.table("users").update({"balance": balance - bet.amount}).eq(
            "id", user_id
        ).execute()
        supabase.table("bets").insert(
            {
                "user_id": user_id,
                "match_id": bet.match_id,
                "amount": bet.amount,
                "odds": bet.odds,
                "prediction": bet.prediction,
            }
        ).execute()

        return {"message": "Bet placed successfully"}

    @staticmethod
    async def delete_bet(bet_id: str, user_id: str, match_id: str):
        print("service bet id", bet_id)
        print("service match", match_id)
        response_match = (
            supabase.table("matches").select("*").eq("fixture_id", match_id).execute()
        )
        match = response_match.data[0]

        response_bet = supabase.table("bets").select("*").eq("id", bet_id).execute()
        bet = response_bet.data[0]

        if match["fixture_status"] != "Not Started":
            raise HTTPException(
                status_code=400, detail="Game has already started or finished"
            )

        print("Bet kann gelöscht werden")
        response_user = supabase.table("users").select("*").eq("id", user_id).execute()
        user = response_user.data[0]
        new_user_balance = user["balance"] + bet["amount"]
        print("old", user["balance"])
        print("new", new_user_balance)

        supabase.table("users").update({"balance": new_user_balance}).eq(
            "id", user_id
        ).execute()
        supabase.table("bets").delete().eq("id", bet_id).execute()

        print("deleted")
        return {"message": "Bet deleted successfully"}

    """ @staticmethod
    async def delete_bet(bet_id: str, user_id: str, match_id: str):
        print("bet service", bet_id)
        print("match service", match_id)
        print("user service", user_id)
        response_bet = supabase.table("bets").select("*").eq("id", bet_id).execute()
        bet = response_bet.data[0]
        bet_amount = bet["amount"]
        response_match = (
            supabase.table("matches").select("*").eq("fixture_id", match_id).execute()
        )
        match = response_match.data[0]
        match_status = match["fixture_status"]

        print("bet bet", bet)
        print("match match", match)

        if match_status != "Not Started":
            raise HTTPException(
                status_code=400, detail="Game has already started or finished"
            )
        response_user = supabase.table("users").select("*").eq("id", user_id).execute()
        user = response_user.data[0]
        user_balance = user["balance"]
        new_user_balance = user_balance + bet_amount

        supabase.table("users").update({"balance": new_user_balance}).eq(
            "id", user_id
        ).execute()
        supabase.table("bets").delete().eq("id", bet_id).execute()

        return {"message": "Bet deleted successfully"} """

    @staticmethod
    async def check_bets():
        open_bets = (
            supabase.table("bets").select("*").eq("status", "open").execute().data
        )

        for bet in open_bets:
            matches = (
                supabase.table("matches")
                .select("*")
                .eq("fixture_id", bet["match_id"])
                .single()
                .execute()
                .data
            )

            if matches["fixture_status"] == "Match Finished":
                prediction = bet["prediction"]
                home_goals = matches["goal_home"]
                away_goals = matches["goal_away"]

                won = (
                    (prediction == "home" and home_goals > away_goals)
                    or (prediction == "away" and home_goals < away_goals)
                    or (prediction == "draw" and home_goals == away_goals)
                )

                if won:
                    user = (
                        supabase.table("users")
                        .select("balance")
                        .eq("id", bet["user_id"])
                        .single()
                        .execute()
                    )
                    user_balance = user.data["balance"]
                    payout = bet["amount"] * bet["odds"]
                    new_balance = user_balance + payout

                    supabase.table("users").update({"balance": new_balance}).eq(
                        "id", bet["user_id"]
                    ).execute()
                supabase.table("bets").update({"status": "won" if won else "lost"}).eq(
                    "id", bet["id"]
                ).execute()
            else:
                print("not started", bet["match_id"])
