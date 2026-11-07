from fastapi import APIRouter, Depends

from app.core.dependencies import get_user_service
from app.core.security import get_current_user
from app.schemas.auth import AuthResponse, LoginRequest, RegisterRequest, UserOut
from app.services.auth_service import AuthService
from app.services.user_service import UserService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=AuthResponse, status_code=201)
async def register(data: RegisterRequest):
    return await AuthService.register(data.email, data.password)


@router.post("/login", response_model=AuthResponse)
async def login(credentials: LoginRequest):
    return await AuthService.login(credentials.email, credentials.password)


@router.get("/me", response_model=UserOut)
def me(
    current_user: dict = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
):
    row = user_service.get_user(current_user["id"])
    return UserOut(user_id=row["id"], username=row["username"], coins=row["coins"])
