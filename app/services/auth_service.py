import httpx
from fastapi import HTTPException, status

from app.core.config import settings
from app.db.supabase_client import supabase
from app.schemas.auth import AuthResponse, UserOut


class AuthService:
    @staticmethod
    async def register_user(id: str, email: str):
        supabase.table("users").insert(
            {"id":  id, "username": email, "balance": 100}
        ).execute()
        return {"message": "User successfully registered"}

    @staticmethod
    async def login(email: str, password: str) -> AuthResponse:
        # 1. Supabase fragen, ob E-Mail und Passwort stimmen
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.supabase_url}/auth/v1/token",
                params={"grant_type": "password"},
                headers={"apikey": settings.supabase_service_key},
                json={"email": email, "password": password},
            )

        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        data = response.json()
        access_token = data["access_token"]
        user_id = data["user"]["id"]

        # 2. Spielerdaten aus unserer eigenen Tabelle laden
        row = (
            supabase.table("users")
            .select("*")
            .eq("id", user_id)
            .single()
            .execute()
            .data
        )

        # 3. Ins Antwort-Schema übersetzen (id -> user_id)
        return AuthResponse(
            access_token=access_token,
            user=UserOut(
                user_id=row["id"],
                username=row["username"],
                balance=row["balance"],
            ),
        )
