from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/matches", tags=["matches"])

""" @router.post("/")
async def add_matches():
    try:
        response = await MatchService.fetch_matches()
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) """