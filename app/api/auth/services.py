from typing import Annotated

from fastapi import Depends, Form

from app.api.auth.exceptions import http_credentials_exception
from app.api.auth.schemas import RefreshTokenRequest, Token, TokenData
from app.api.auth.utils import authenticate_user, generate_tokens, refresh_tokens, verify_refresh_token
from app.api.users.schemas import UserByUsernameRequest
from app.api.users.utils import user_by_username
from app.database import SessionDep
from app.models import User


async def user_by_username_form(
    username: Annotated[str, Form()],
    session: SessionDep,
) -> User:
    return await user_by_username(
        UserByUsernameRequest(username=username),
        session,
    )


def auth_user(
    password: Annotated[str, Form()],
    user: User = Depends(user_by_username_form),
):
    return authenticate_user(user, password)


def create_tokens(user: User = Depends(auth_user)) -> Token:
    return Token(**generate_tokens(user))


def get_token_data(refresh_token_data: RefreshTokenRequest) -> TokenData:
    token_data = verify_refresh_token(refresh_token_data.token)
    if not token_data:
        raise http_credentials_exception

    return token_data


def refresh_token(token_data: TokenData = Depends(get_token_data)) -> Token:
    return Token(**refresh_tokens(token_data))
