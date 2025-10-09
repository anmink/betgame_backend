from fastapi import APIRouter, HTTPException
from typing import List
from app.models.match import Match
from app.services.match_service import MatchService

router = APIRouter(prefix="/matches", tags=["matches"])

@router.post("/")
async def add_matches():
    try:
        response = await MatchService.save_matches()
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    