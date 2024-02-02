from fastapi import Depends
from pydantic import conint

from app.api.common.services import BaseService
from app.api.common.utils import PaginationDep
from app.api.products.repository import ProductRepository
from app.api.products.schemas import ProductCreateSchemas, ProductQueryParams, ProductUpdateSchemas
from app.database import SessionDep
from app.models import Product


class ProductService(BaseService):
    repository = ProductRepository

    @classmethod
    async def create(
        cls,
        data: ProductCreateSchemas,
        session: SessionDep,
    ) -> Product | None:
        return await super().create(data, session)

    @classmethod
    async def get(cls, product_id: conint(gt=0), session: SessionDep) -> Product | None:
        return await super().get(product_id, session)

    @classmethod
    async def get_many(
        cls,
        pagination: PaginationDep,
        session: SessionDep,
    ) -> list[Product] | None:
        return await super().get_many(pagination, session)

    @classmethod
    async def get_many_query(
        cls,
        session: SessionDep,
        pagination: PaginationDep,
        query_params_product: ProductQueryParams = Depends(ProductQueryParams),
    ):
        return await super().get_many_query(
            session,
            pagination,
            query_params_product,
        )

    @classmethod
    async def edit(
        cls,
        product_id: conint(gt=0),
        data: ProductUpdateSchemas,
        session: SessionDep,
    ):
        return await super().edit(product_id, data, session)

    @classmethod
    async def delete(cls, product_id: conint(gt=0), session: SessionDep):
        return await super().delete(product_id, session)
