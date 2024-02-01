"""Слой работы бд"""

from abc import ABC
from collections.abc import Mapping
from typing import Self

import sqlalchemy
from sqlalchemy import ColumnElement

from app.database import Base


class BaseSearchMixin(ABC):
    model: type[Base]

    @classmethod
    def search(cls, **kwargs) -> sqlalchemy.Select:
        """Возвращает селект для одного результата поиска по полям."""

        select = sqlalchemy.select(cls.model).filter_by(**kwargs)

        if hasattr(cls.model, "is_deleted"):
            return select.filter_by(is_deleted=False)

        return select


class BaseRepository:
    model: type[Base]

    @classmethod
    def select(cls, obj_id: int) -> sqlalchemy.Select:
        """Возвращает селект для одного результата по айди."""

        select = sqlalchemy.select(cls.model).filter_by(id=obj_id)
        if hasattr(cls.model, "is_deleted"):
            return select.filter_by(is_deleted=False)

        return select

    @classmethod
    def select_many(cls, obj_filter: Mapping | None = None) -> sqlalchemy.Select:
        """Возвращает селект для множества результатов по фильтру."""

        select = sqlalchemy.select(cls.model)

        if hasattr(cls.model, "is_deleted"):
            select = select.filter_by(is_deleted=False)

        if obj_filter is None:
            return select

        return select.filter_by(**obj_filter)

    @classmethod
    def insert(cls, obj_data: Mapping, **extra_fields) -> sqlalchemy.Insert:
        """Возвращает инсерт для одного элемента."""

        return (
            sqlalchemy.insert(cls.model)
            .values(**obj_data, **extra_fields)
            .returning(
                cls.model,
            )
        )

    @classmethod
    def delete(cls, obj_id: int) -> sqlalchemy.Delete | sqlalchemy.Update:
        """
        Возвращает делит для одного элемента.
        Если модель имеет поле is_deleted (safe delete) -
        возвращает апдейт.
        """
        where_clause = cls.model.id == obj_id
        if hasattr(cls.model, "is_deleted"):
            return sqlalchemy.update(cls.model).where(where_clause).values(is_deleted=True).returning(cls.model)

        return (
            sqlalchemy.delete(cls.model)
            .where(where_clause)
            .returning(
                cls.model,
            )
        )

    @classmethod
    def update(
        cls,
        obj_id: int,
        update_fields: Mapping,
        **extra_fields,
    ) -> sqlalchemy.Update:
        """Возвращает апдейт для элементов по айди."""

        return (
            sqlalchemy.update(cls.model)
            .filter_by(id=obj_id)
            .values(**update_fields, **extra_fields)
            .returning(cls.model)
        )

    @classmethod
    def for_model(cls, model) -> type[Self]:
        """Возвращает подкласс с базовыми методами для модели."""

        return type(
            model.__name__ + "Repository",
            (cls,),
            {"model": model},
        )


class DependableBaseRepository(BaseRepository):
    """Поле прямой зависимости,
    dependency_field - от какого поля зависимость/ содержит ForeignKey"""

    #    пример
    #     class Post(Base):
    #         __tablename__ = 'posts'
    #         username = Column(String)
    #         id = Column(Integer, primary_key=True)
    #         user_id = Column(Integer, ForeignKey('users.id'))
    #
    #
    #     class PostRepository(DependableBaseRepository):
    #         model = Post
    #         dependency_field = Post.user_id

    dependency_field: ColumnElement

    @classmethod
    def select(
        cls,
        obj_id: int,
        dep_id=None,
    ) -> sqlalchemy.Select:
        select = super().select(obj_id)

        if dep_id is None:
            return select

        return select.where(cls.dependency_field == dep_id)

    @classmethod
    def select_many(
        cls,
        dep_id=None,
        obj_filter: Mapping | None = None,
    ) -> sqlalchemy.Select:
        select = super().select_many(obj_filter)

        if dep_id is None:
            return select

        return select.where(cls.dependency_field == dep_id)

    @classmethod
    def insert(
        cls,
        obj_data: Mapping,
        dep_id=None,
        **extra_fields,
    ) -> sqlalchemy.Insert:
        if dep_id is not None:
            extra_fields = extra_fields | {cls.dependency_field.key: dep_id}

        return super().insert(obj_data, **extra_fields)

    @classmethod
    def update(
        cls,
        obj_id,
        update_fields: Mapping,
        dep_id=None,
        **extra_fields,
    ) -> sqlalchemy.Update:
        update = super().update(obj_id, update_fields, **extra_fields)
        return update.where(cls.dependency_field == dep_id)

    @classmethod
    def delete(
        cls,
        obj_id: int,
        dep_id=None,
    ) -> sqlalchemy.Delete | sqlalchemy.Update:
        delete = super().delete(obj_id)

        if not dep_id:
            return delete

        return delete.where(cls.dependency_field == dep_id)
