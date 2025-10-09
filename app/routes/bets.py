from fastapi import APIRouter, HTTPException
from app.services.bet_service import BetService
from app.models.bet import Bet

router = APIRouter(prefix="/bets", tags=["bets"])

@router.post("/")
def place_bet(bet: Bet):
    try:
        result = BetService.place_bet(
            user_id=bet.user_id,
            match_id=bet.match_id,
            amount=bet.amount,
            odds=bet.odds
        )
        return {"success": True, "bet": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))