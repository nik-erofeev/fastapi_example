from pydantic import conint
from sqlalchemy.exc import IntegrityError

from app.api.auth.utils import pwd_context
from app.api.common.services import BaseService
from app.api.common.utils import PaginationDep
from app.api.users.exceptions import http_data_conflict_exception, http_user_not_found_exception
from app.api.users.repository import UserRepository
from app.api.users.schemas import UserChangePasswordRequest, UserCreateSchemas, UserUpdateSchemas
from app.database import SessionDep


class GeneratePasswordService:
    @staticmethod
    def hash_password(password):
        return pwd_context.hash(password)


class UserService(BaseService, GeneratePasswordService):
    repository = UserRepository

    @classmethod
    async def create(cls, data: UserCreateSchemas, session: SessionDep):
        data.password = cls.hash_password(data.password)

        try:
            user = await super().create(data, session)
        except IntegrityError:
            raise http_data_conflict_exception
        return user

    @classmethod
    async def get(cls, user_id: conint(gt=0), session: SessionDep):
        user = await super().get(user_id, session)
        if user is None:
            raise http_user_not_found_exception
        return user

    @classmethod
    async def get_many(cls, pagination: PaginationDep, session: SessionDep):
        return await super().get_many(pagination, session)

    @classmethod
    async def edit(cls, user_id: conint(gt=0), data: UserUpdateSchemas, session: SessionDep):
        user = await super().get(user_id, session)
        if user is None:
            raise http_user_not_found_exception

        try:
            user_update = await super().edit(user_id, data, session)
        except IntegrityError:
            raise http_data_conflict_exception

        return user_update

    @classmethod
    async def delete(cls, user_id: conint(gt=0), session: SessionDep):
        user = await super().get(user_id, session)
        if user is None:
            raise http_user_not_found_exception

        return await super().delete(user_id, session)

    @classmethod
    async def change_password(
        cls,
        user_id: conint(gt=0),
        data: UserChangePasswordRequest,
        session: SessionDep,
    ):
        data = data.model_dump()
        update = cls.repository.update(
            user_id,
            {},
            password=cls.hash_password(data["new_password"]),
        )

        update = await session.scalar(update)
        await session.flush()

        return update

    @classmethod
    @property
    def change_password_dep(cls):
        return cls._dep_get(cls.change_password)
