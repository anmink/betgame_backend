# app/services/bet_service.py
from datetime import UTC, datetime

from app.core.errors import BettingClosedError, NotFoundError
from app.db.supabase_client import supabase
from app.repositories.bet_repository import BetRepository
from app.repositories.match_repository import MatchRepository
from app.schemas.bet import BetCreate
from app.services.betting_rules import calculate_payout, is_betting_open, is_winning, odds_for

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
    async def cancel_bet(bet_id: int, user_id: str):
        bet_repository.cancel(user_id, bet_id)

    @staticmethod
    async def check_bets():
        for bet in bet_repository.list_open():
            match = match_repository.get_by_id(bet["match_id"])
            if match is None or match["fixture_status"] != "Match Finished":
                continue

            won = is_winning(bet["prediction"], match["goal_home"], match["goal_away"])
            payout = calculate_payout(bet["stake"], bet["odds"]) if won else 0
            bet_repository.settle(bet["id"], won, payout)
