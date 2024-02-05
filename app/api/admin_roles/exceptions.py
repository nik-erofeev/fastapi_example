from fastapi import HTTPException
from starlette import status


http_current_user_conflict_exception = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Вы не может управлять привилегиями",
)
http_admin_or_superadmin_conflict_exception = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Пользователь уже является админом или суперадмином",
)
http_no_admin_or_superadmin_conflict_exception = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Пользователь не является админом",
)
