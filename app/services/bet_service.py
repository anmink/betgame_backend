# app/services/bet_service.py
from datetime import UTC, datetime

from fastapi import HTTPException

from app.core.errors import BettingClosedError, NotFoundError
from app.db.supabase_client import supabase
from app.repositories.bet_repository import BetRepository
from app.repositories.match_repository import MatchRepository
from app.schemas.bet import BetCreate
from app.services.betting_rules import is_betting_open, odds_for

match_repository = MatchRepository()
bet_repository = BetRepository()


class BetService:
    @staticmethod
    async def get_bets(user_id: str):
        try:
            response = (
                supabase.from_("bets")
                .select(
                    """
                    id,
                    stake,
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
                key=lambda bet: bet["matches"]["fixture_date"] if bet.get("matches") else "",
                reverse=True,  # Neueste/Jüngste Datum zuerst
            )

            return sorted_bets

        except Exception as e:
            raise Exception(f"Error fetching bets: {e}") from e

    @staticmethod
    async def place_bet(bet: BetCreate, user_id: str):
        match = match_repository.get_by_id(bet.match_id)
        if match is None:
            raise NotFoundError("Match not found")
        if not is_betting_open(match, datetime.now(UTC)):
            raise BettingClosedError("Betting is closed for this match")
        odds = odds_for(match, bet.prediction)

        bet_id = bet_repository.place(user_id, bet.match_id, bet.stake, bet.prediction, odds)

        return {"bet_id": bet_id}

    @staticmethod
    async def delete_bet(bet_id: str, user_id: str, match_id: str):
        response_match = supabase.table("matches").select("*").eq("fixture_id", match_id).execute()
        match = response_match.data[0]

        response_bet = supabase.table("bets").select("*").eq("id", bet_id).execute()
        bet = response_bet.data[0]

        if match["fixture_status"] != "Not Started":
            raise HTTPException(status_code=400, detail="Game has already started or finished")

        response_user = supabase.table("users").select("*").eq("id", user_id).execute()
        user = response_user.data[0]
        new_user_coins = user["coins"] + bet["stake"]

        supabase.table("users").update({"coins": new_user_coins}).eq("id", user_id).execute()
        supabase.table("bets").delete().eq("id", bet_id).execute()

        return {"message": "Bet deleted successfully"}

    @staticmethod
    async def check_bets():
        open_bets = supabase.table("bets").select("*").eq("status", "open").execute().data

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
                        .select("coins")
                        .eq("id", bet["user_id"])
                        .single()
                        .execute()
                    )
                    user_coins = user.data["coins"]
                    payout = bet["stake"] * bet["odds"]
                    new_coins = user_coins + payout

                    supabase.table("users").update({"coins": new_coins}).eq(
                        "id", bet["user_id"]
                    ).execute()
                supabase.table("bets").update({"status": "won" if won else "lost"}).eq(
                    "id", bet["id"]
                ).execute()
