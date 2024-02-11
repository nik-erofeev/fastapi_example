"""Константы для ресурса "Пользователи" """

from datetime import timedelta

from app.config import settings


ACCESS_TOKEN_EXPIRES: timedelta = timedelta(
    minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
)

REFRESH_TOKEN_EXPIRES: timedelta = timedelta(
    minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES,
)
