from fastapi import APIRouter, HTTPException
from app.services.bet_service import BetService

router = APIRouter(prefix="/matches", tags=["matches"])

@router.get("/")
async def get_bets(user_id: str):
    try:
        response = await BetService.get_bets(user_id=user_id)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/")
async def place_bet(user_id: str):
    try:
        response = await BetService.place_bet(user_id=user_id)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.delete("/{bet_id}")
async def delete_bet(bet_id: str, user_id: str):
    try:
        response = await BetService.delete_bet(bet_id=bet_id, user_id=user_id)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))