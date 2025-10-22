from fastapi import APIRouter, HTTPException
from app.services.match_service import MatchService

router = APIRouter(prefix="/matches", tags=["matches"])

@router.get("/")
async def get_matches():
    try:
        response = await MatchService.get_matches()
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))