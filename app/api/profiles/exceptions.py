from fastapi import HTTPException, status


http_uniq_profile_exception = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Профиль пользователя уже существует",
)
