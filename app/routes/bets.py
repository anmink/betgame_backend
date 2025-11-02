from fastapi import APIRouter, HTTPException, Depends
from app.middleware.auth_dependency import get_current_user
from app.services.bet_service import BetService
from app.models.bet import Bet


router = APIRouter(prefix="/bets", tags=["bets"])

""" @router.get("/{user_id}")
async def get_betCollection(user_id: str):
    try:
        response = await BetService.get_bets(user_id=user_id)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) """
    
@router.get("/")
async def get_betCollection():
    try:
        user_id = "f17e2687-487f-48a9-a1d0-34cb370f68ec"
        response = await BetService.get_bets(user_id)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

""" @router.post("/")
async def place_bet(user_id: str):
    try:
        response = await BetService.place_bet(user_id=user_id)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) """
    
""" @router.post("/")
async def place_bet(bet: Bet):
    try:
        #user_id = "f17e2687-487f-48a9-a1d0-34cb370f68ec"
        response = await BetService.place_bet(bet=bet, user_id=user_id)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) """

@router.post("/")
async def place_bet(bet: Bet, current_user: dict = Depends(get_current_user)):
    try:
        user_id = current_user["id"]
        response = await BetService.place_bet(bet, user_id)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    
@router.delete("/")
async def delete_bet(bet_id: str, user_id: str):
    try:
        #user_id = "f17e2687-487f-48a9-a1d0-34cb370f68ec"
        #bet_id = "100cd895-7e9a-49ec-a838-99122556accf"
        response = await BetService.delete_bet(bet_id=bet_id, user_id=user_id)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))