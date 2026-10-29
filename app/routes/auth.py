from fastapi import APIRouter, HTTPException, Depends
from app.core.security import get_current_user
from app.services.user_service import UserService
from app.services.auth_service import AuthService
from app.schemas.auth import AuthResponse, LoginRequest, UserOut

router = APIRouter(prefix="/auth", tags=["Auth"])


# Registrierung
@router.post("/register")
async def register_user(data: dict):
    try:
        user_id = data["user_id"]
        email = data["email"]
        result = await AuthService.register_user(user_id, email)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login", response_model=AuthResponse)
async def login(credentials: LoginRequest):
    return await AuthService.login(credentials.email, credentials.password)

@router.get("/me", response_model=UserOut)
async def me(current_user: dict = Depends(get_current_user)):
    row = await UserService.get_user(current_user["id"])
    return UserOut(user_id=row["id"], username=row["username"], balance=row["balance"])