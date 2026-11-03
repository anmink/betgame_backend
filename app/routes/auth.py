from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.services.user_service import UserService
from app.services.auth_service import AuthService
from app.schemas.auth import AuthResponse, LoginRequest, UserOut, RegisterRequest

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=AuthResponse, status_code=201)
async def register(data: RegisterRequest):
    return await AuthService.register(data.email, data.password)

@router.post("/login", response_model=AuthResponse)
async def login(credentials: LoginRequest):
    return await AuthService.login(credentials.email, credentials.password)

@router.get("/me", response_model=UserOut)
async def me(current_user: dict = Depends(get_current_user)):
    row = await UserService.get_user(current_user["id"])
    return UserOut(user_id=row["id"], username=row["username"], balance=row["balance"])