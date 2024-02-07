from datetime import timedelta

from pydantic import BaseModel

from app.api.users.schemas import UserByUsernameRequest


class TokenData(BaseModel):
    sub: str | None = None
    user_id: int | None = None
    exp: timedelta | None = None


class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str


class UserPasswordAuthenticationRequest(UserByUsernameRequest):
    password: str


class RefreshTokenRequest(BaseModel):
    token: str
