from fastapi import APIRouter, Depends, HTTPException

from app.core.security import get_current_user
from app.services.user_service import UserService

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/")
async def get_user(current_user: dict = Depends(get_current_user)):
    try:
        user_id = current_user["id"]
        response = await UserService.get_user(user_id)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
