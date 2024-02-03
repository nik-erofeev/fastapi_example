from typing import Annotated

from fastapi import Depends
from pydantic import conint
from sqlalchemy.exc import IntegrityError

from app.api.common.services import DependableBaseService
from app.api.common.utils import PaginationDep
from app.api.profiles.exceptions import http_uniq_profile_exception
from app.api.profiles.repository import ProfileRepository
from app.api.profiles.schemas import ProfileCreateSchemas, ProfileUpdateSchemas
from app.api.users.services import UserService
from app.database import SessionDep
from app.models import Profile, User


UserDep = Annotated[User, Depends(UserService.get)]


class ProfileService(DependableBaseService):
    repository = ProfileRepository

    @classmethod
    async def create(
        cls,
        data: ProfileCreateSchemas,
        user: UserDep,
        session: SessionDep,
    ) -> Profile | None:
        try:
            return await super().create(data, user, session)
        except IntegrityError:
            raise http_uniq_profile_exception

    @classmethod
    async def get(
        cls,
        profile_id: conint(gt=0),
        user: UserDep,
        session: SessionDep,
    ) -> Profile | None:
        return await super().get(profile_id, user, session)

    @classmethod
    async def get_many(
        cls,
        pagination: PaginationDep,
        user: UserDep,
        session: SessionDep,
    ) -> list[Profile] | None:
        return await super().get_many(pagination, user, session)

    @classmethod
    async def edit(
        cls,
        profile_id: conint(gt=0),
        data: ProfileUpdateSchemas,
        user: UserDep,
        session: SessionDep,
    ):
        return await super().edit(profile_id, data, user, session)

    @classmethod
    async def delete(cls, profile_id: conint(gt=0), user: UserDep, session: SessionDep):
        return await super().delete(profile_id, user, session)
