from fastapi import APIRouter, HTTPException, Request
from app.services.auth_service import AuthService
import requests
import os

router = APIRouter(prefix="/auth", tags=["Auth"])


# Registrierung
@router.post("/register")
async def register_user(data: dict):
    try:
        user_id = data["user_id"]
        email = data["email"]
        print(user_id, email)
        result = await AuthService.register_user(user_id, email)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Token Validierung (geschützte Route)
@router.get("/validate")
async def validate_token(request: Request):
    token = request.headers.get("Authorization")
    print("token", token)
    if not token:
        print("validate: missing Authorization header")
        raise HTTPException(status_code=401, detail="Missing token")

    if not token.lower().startswith("bearer "):
        token = f"Bearer {token}"

    # Supabase Token prüfen
    response = requests.get(
        f"{os.getenv('SUPABASE_URL')}/auth/v1/user",
        headers={"Authorization": token, "apikey": os.getenv("SUPABASE_KEY")},
    )

    if response.status_code != 200:
        print("validate: supabase rejected", response.status_code, response.text)
        raise HTTPException(status_code=401, detail="Invalid token")

    user_data = response.json()
    return {"user": user_data}
