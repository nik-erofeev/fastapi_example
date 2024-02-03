from abc import ABC, abstractmethod
from collections.abc import Mapping
from typing import Annotated

from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy import ColumnElement

from app.api.common.repository import BaseRepository, DependableBaseRepository
from app.api.common.utils import paginate_select, PaginationDep
from app.database import SessionDep
from app.models import IdMixin


class AbstractBaseService(ABC):
    repository: type[BaseRepository]

    @classmethod
    def _dep_get(cls, func):
        return Annotated[cls.repository.model, Depends(func)]

    @classmethod
    @property
    def get_dep(cls):
        return cls._dep_get(cls.get)

    @classmethod
    @property
    def get_many_dep(cls):
        return cls._dep_get(cls.get_many)

    @classmethod
    @property
    def get_many_query_dep(cls):
        return cls._dep_get(cls.get_many_query)

    @classmethod
    @property
    def create_dep(cls):
        return cls._dep_get(cls.create)

    @classmethod
    @property
    def edit_dep(cls):
        return cls._dep_get(cls.edit)

    @classmethod
    @property
    def delete_dep(cls):
        return cls._dep_get(cls.delete)

    @classmethod
    @abstractmethod
    async def create(cls, *args, **kwargs):
        pass

    @classmethod
    @abstractmethod
    async def get(cls, *args, **kwargs):
        pass

    @classmethod
    @abstractmethod
    async def get_many(cls, *args, **kwargs):
        pass

    @classmethod
    @abstractmethod
    async def get_many_query(cls, *args, **kwargs):
        pass

    @classmethod
    @abstractmethod
    async def edit(cls, *args, **kwargs):
        pass

    @classmethod
    @abstractmethod
    async def delete(cls, *args, **kwargs):
        pass


class BaseService(AbstractBaseService):
    repository: type[BaseRepository]

    @classmethod
    async def _create(cls, data: BaseModel, session: SessionDep):
        data = data.model_dump()
        insert = cls.repository.insert(data)

        result = await session.scalar(insert)
        await session.flush()

        return result

    @classmethod
    async def _get(cls, obj_id: int, session: SessionDep):
        select = cls.repository.select(obj_id)

        result = await session.scalar(select)

        return result

    @classmethod
    async def _get_many(cls, pagination: PaginationDep, session: SessionDep):
        select = cls.repository.select_many()
        paginated = paginate_select(select, pagination)

        result = await session.scalars(paginated)

        return result.all()

    @classmethod
    async def _get_many_query(
        cls,
        session: SessionDep,
        pagination: PaginationDep | None = None,
        query_params=None,
    ):
        if query_params:
            query_params = query_params.model_dump(exclude_defaults=True)

        select = cls.repository.select_many(query_params)
        if pagination:
            select = paginate_select(select, pagination)

        result = await session.scalars(select)
        return result.all()

    @classmethod
    async def _edit(cls, obj_id: int, data: BaseModel, session: SessionDep):
        update = cls.repository.update(
            obj_id,
            data.model_dump(exclude_unset=True),
        )

        result = await session.scalar(update)

        await session.flush()

        return result

    @classmethod
    async def _delete(cls, obj_id: int, session: SessionDep):
        delete = cls.repository.delete(obj_id)

        result = await session.scalar(delete)

        await session.flush()

        return result

    @classmethod
    async def create(cls, *args, **kwargs):
        return await cls._create(*args, **kwargs)

    @classmethod
    async def get(cls, *args, **kwargs):
        return await cls._get(*args, **kwargs)

    @classmethod
    async def get_many(cls, *args, **kwargs):
        return await cls._get_many(*args, **kwargs)

    @classmethod
    async def get_many_query(cls, *args, **kwargs):
        return await cls._get_many_query(*args, **kwargs)

    @classmethod
    async def edit(cls, *args, **kwargs):
        return await cls._edit(*args, **kwargs)

    @classmethod
    async def delete(cls, *args, **kwargs):
        return await cls._delete(*args, **kwargs)


class DependableBaseService(AbstractBaseService):
    repository: type[DependableBaseRepository]
    dependency_field: ColumnElement = IdMixin.id

    @classmethod
    def _get_dep_value(cls, obj):
        if isinstance(obj, Mapping):
            return obj[cls.dependency_field.name]

    @classmethod
    async def _create(cls, data: BaseModel, dep, session: SessionDep):
        data = data.model_dump()
        insert = cls.repository.insert(data, cls._get_dep_value(dep))

        result = await session.scalar(insert)
        await session.flush()

        return result

    @classmethod
    async def _get(cls, obj_id: int, dep, session: SessionDep):
        select = cls.repository.select(obj_id, cls._get_dep_value(dep))

        result = await session.scalar(select)

        return result

    @classmethod
    async def _get_many(cls, pagination: PaginationDep, dep, session: SessionDep):
        select = cls.repository.select_many(cls._get_dep_value(dep))
        paginated = paginate_select(select, pagination)

        result = await session.scalars(paginated)

        return result.all()

    @classmethod
    async def _edit(cls, obj_id: int, data: BaseModel, dep, session: SessionDep):
        update = cls.repository.update(
            obj_id,
            data.model_dump(exclude_unset=True),
            cls._get_dep_value(dep),
        )

        result = await session.scalar(update)

        await session.flush()

        return result

    @classmethod
    async def _delete(cls, obj_id: int, dep, session: SessionDep):
        delete = cls.repository.delete(obj_id, cls._get_dep_value(dep))

        result = await session.scalar(delete)

        await session.flush()

        return result

    @classmethod
    async def create(cls, *args, **kwargs):
        return await cls._create(*args, **kwargs)

    @classmethod
    async def get(cls, *args, **kwargs):
        return await cls._get(*args, **kwargs)

    @classmethod
    async def get_many(cls, *args, **kwargs):
        return await cls._get_many(*args, **kwargs)

    @classmethod
    async def edit(cls, *args, **kwargs):
        return await cls._edit(*args, **kwargs)

    @classmethod
    async def delete(cls, *args, **kwargs):
        return await cls._delete(*args, **kwargs)

    @classmethod
    async def get_many_query(cls):
        raise NotImplementedError
