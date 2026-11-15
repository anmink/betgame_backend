from fastapi import APIRouter, Depends, HTTPException

from app.core.security import get_current_user
from app.schemas.bet import BetCreate
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


@router.post("/", status_code=201)
async def place_bet(bet: BetCreate, current_user: dict = Depends(get_current_user)):
    return await BetService.place_bet(bet, current_user["id"])


@router.delete("/")
async def delete_bet(bet_id: str, match_id: str, current_user: dict = Depends(get_current_user)):
    try:
        user_id = current_user["id"]
        response = await BetService.delete_bet(bet_id=bet_id, user_id=user_id, match_id=match_id)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
