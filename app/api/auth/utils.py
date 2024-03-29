from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from jose.exceptions import ExpiredSignatureError
from passlib.context import CryptContext

from app.api.auth.constanct import ACCESS_TOKEN_EXPIRES, REFRESH_TOKEN_EXPIRES
from app.api.auth.exceptions import (
    http_credentials_exception,
    http_expire_exception,
    http_incorrect_username_or_password_exception,
    http_token_absent_exception,
)
from app.api.auth.schemas import TokenData
from app.api.users.schemas import UserByUsernameRequest
from app.api.users.utils import user_by_username
from app.config import settings
from app.database import SessionDep
from app.models import User


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


def verify_user_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(user: User, password: str) -> User | None:
    if user and verify_user_password(password, user.password):
        return user


def create_token(data: dict, expires_delta: timedelta, secret: str) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, key=secret, algorithm=settings.ALGORITHM)
    return encode_jwt


def verify_refresh_token(token: str):
    try:
        payload = jwt.decode(
            token,
            key=settings.REFRESH_SECRET_KEY,
            algorithms=settings.ALGORITHM,
        )

        username: str = payload.get("sub")
        user_id = payload.get("user_id")
        exp = payload.get("exp")
        if username is None or user_id is None:
            raise http_credentials_exception

        token_data = TokenData(sub=username, user_id=user_id, exp=exp)

    except ExpiredSignatureError:
        raise http_expire_exception

    except JWTError:
        raise http_credentials_exception

    return token_data


def generate_tokens(user: User) -> dict:
    if user is None:
        raise http_incorrect_username_or_password_exception

    access_token = create_token(
        data={"sub": user.username, "user_id": user.id},
        expires_delta=ACCESS_TOKEN_EXPIRES,
        secret=settings.JWT_SECRET_KEY,
    )

    refresh_token = create_token(
        data={"sub": user.username, "user_id": user.id},
        expires_delta=REFRESH_TOKEN_EXPIRES,
        secret=settings.REFRESH_SECRET_KEY,
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token,
    }


def refresh_tokens(refresh_data: TokenData) -> dict:
    access_token = create_token(
        data=refresh_data.model_dump(),
        expires_delta=ACCESS_TOKEN_EXPIRES,
        secret=settings.JWT_SECRET_KEY,
    )

    refresh_token = create_token(
        data=refresh_data.model_dump(),
        expires_delta=REFRESH_TOKEN_EXPIRES,
        secret=settings.REFRESH_SECRET_KEY,
    )

    return {
        "access_token": access_token,
        "token_type": "Bearer",
        "refresh_token": refresh_token,
    }


async def decode_token(token: str) -> UserByUsernameRequest:
    try:
        payload = jwt.decode(
            token,
            key=settings.JWT_SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        username: str = payload.get("sub")
        if username is None:
            raise http_credentials_exception
        user = UserByUsernameRequest(username=username)
        return user

    except ExpiredSignatureError:
        raise http_expire_exception
    except JWTError:
        raise http_credentials_exception


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: SessionDep,
) -> User:
    username = await decode_token(token)
    user = await user_by_username(username, session)
    return user


def get_token_cookie(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise http_token_absent_exception
    return token


async def get_current_user_from_cookie(
    session: SessionDep,
    token: str = Depends(get_token_cookie),
) -> User:
    username = await decode_token(token)

    user = await user_by_username(username, session)
    return user
