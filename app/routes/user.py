from fastapi import APIRouter, Depends

from app.core.dependencies import get_user_service
from app.core.security import get_current_user
from app.services.user_service import UserService

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/")
def get_user(
    current_user: dict = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
):
    return user_service.get_user(current_user["id"])
