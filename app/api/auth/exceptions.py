"""Исключения для ресурса "Пользователи" """
from fastapi import HTTPException, status


http_credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Не удается проверить учетные данные",
    headers={"WWW-Authenticate": "Bearer"},
)


http_incorrect_username_or_password_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Неправильный логин или пароль",
    headers={"WWW-Authenticate": "Bearer"},
)

http_expire_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Срок действия токена истек",
)

http_token_absent_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Cookie отсутствует",
)
