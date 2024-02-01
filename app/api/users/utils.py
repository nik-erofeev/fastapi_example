from fastapi import HTTPException, status
from sqlalchemy.exc import NoResultFound

from app.api.users.repository import UserRepository
from app.api.users.schemas import UserByUsernameRequest
from app.database import SessionDep


async def user_by_username(
    user_data: UserByUsernameRequest,
    session: SessionDep,
):
    search_select = UserRepository.search(username=user_data.username)

    result = await session.scalar(search_select)

    try:
        return result

    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь с указанным именем пользователя не найден",
        )
