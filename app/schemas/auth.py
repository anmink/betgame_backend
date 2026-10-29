from pydantic import BaseModel, Field

class LoginRequest(BaseModel):
    email: str
    password: str = Field(min_length=6)

class UserOut(BaseModel):
    user_id: str
    username: str
    balance: float

class AuthResponse(BaseModel):
    access_token: str
    user: UserOut