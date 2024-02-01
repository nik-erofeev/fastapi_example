from fastapi import HTTPException, status


http_data_conflict_exception = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Пользователь с таким именем username/email уже существует",
)
