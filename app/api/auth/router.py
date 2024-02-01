"""Контроллеры для ресурса "Пользователи" """
from fastapi import APIRouter, Depends, status

from app.api.auth.schemas import Token
from app.api.auth.services import create_tokens, refresh_token


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/token", response_model=Token, status_code=status.HTTP_201_CREATED)
async def login_for_access_token(token: Token = Depends(create_tokens)):
    return token


@router.post("/refresh", response_model=Token, status_code=status.HTTP_201_CREATED)
async def get_new_tokens(token: Token = Depends(refresh_token)):
    return token
