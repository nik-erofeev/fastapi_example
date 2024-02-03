from typing import Annotated

from fastapi import Depends
from pydantic import conint

from app.api.common.services import DependableBaseService
from app.api.common.utils import PaginationDep
from app.api.posts.repository import PostRepository
from app.api.posts.schemas import PostCreateSchemas, PostUpdateSchemas
from app.api.users.services import UserService
from app.database import SessionDep
from app.models import Post, User


UserDep = Annotated[User, Depends(UserService.get)]


class PostService(DependableBaseService):
    repository = PostRepository

    @classmethod
    async def create(
        cls,
        data: PostCreateSchemas,
        user: UserDep,
        session: SessionDep,
    ) -> Post | None:
        return await super().create(data, user, session)

    @classmethod
    async def get(
        cls,
        post_id: conint(gt=0),
        user: UserDep,
        session: SessionDep,
    ) -> Post | None:
        return await super().get(post_id, user, session)

    @classmethod
    async def get_many(
        cls,
        pagination: PaginationDep,
        user: UserDep,
        session: SessionDep,
    ) -> list[Post] | None:
        return await super().get_many(pagination, user, session)

    @classmethod
    async def edit(
        cls,
        post_id: conint(gt=0),
        data: PostUpdateSchemas,
        user: UserDep,
        session: SessionDep,
    ):
        return await super().edit(post_id, data, user, session)

    @classmethod
    async def delete(cls, post_id: conint(gt=0), user: UserDep, session: SessionDep):
        return await super().delete(post_id, user, session)
