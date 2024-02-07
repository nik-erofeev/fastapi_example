"""Контроллеры для ресурса "Пользователи" """
from fastapi import APIRouter, Depends, Response, status

from app.api.auth.schemas import Token
from app.api.auth.services import create_tokens, refresh_token
from app.api.auth.utils import get_current_user_from_cookie
from app.api.users.schemas import UserByUsernameRequest
from app.models import User


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/token", response_model=Token, status_code=status.HTTP_201_CREATED)
async def login_for_access_token(response: Response, token: Token = Depends(create_tokens)):
    response.set_cookie(key="access_token", value=token.access_token)
    return token


@router.post("/refresh", response_model=Token, status_code=status.HTTP_201_CREATED)
async def get_new_tokens(response: Response, token: Token = Depends(refresh_token)):
    response.set_cookie(key="access_token", value=token.refresh_token)
    return token


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("access_token")
    return {"сообщение": "Успешный выход из системы"}


@router.get("/me", status_code=status.HTTP_200_OK, response_model=UserByUsernameRequest)
async def read_user_for_cookie(current_user: User = Depends(get_current_user_from_cookie)):
    return current_user
