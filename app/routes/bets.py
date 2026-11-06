from fastapi import APIRouter, Depends, HTTPException

from app.core.security import get_current_user
from app.models.bet import Bet
from app.services.bet_service import BetService

router = APIRouter(prefix="/bets", tags=["bets"])


@router.get("/")
async def get_bets(current_user: dict = Depends(get_current_user)):
    try:
        user_id = current_user["id"]
        response = await BetService.get_bets(user_id)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/")
async def place_bet(bet: Bet, current_user: dict = Depends(get_current_user)):
    try:
        user_id = current_user["id"]
        response = await BetService.place_bet(bet, user_id)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.delete("/")
async def delete_bet(bet_id: str, match_id: str, current_user: dict = Depends(get_current_user)):
    try:
        user_id = current_user["id"]
        response = await BetService.delete_bet(bet_id=bet_id, user_id=user_id, match_id=match_id)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
