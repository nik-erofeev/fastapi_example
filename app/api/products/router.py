from fastapi import APIRouter, status

from app.api.products.schemas import ProductResponseSchemas
from app.api.products.services import ProductService


router = APIRouter(
    prefix="/products",
    tags=["products"],
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ProductResponseSchemas,
)
async def create_product(product: ProductService.create_dep):
    return product


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[ProductResponseSchemas],
)
async def get_many_users(product: ProductService.get_many_query_dep):
    return product


@router.get(
    "/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=ProductResponseSchemas,
)
async def get_product(product: ProductService.get_dep):
    return product


@router.patch(
    "/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=ProductResponseSchemas,
)
async def edit_product(product: ProductService.edit_dep):
    return product


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=ProductResponseSchemas,
)
async def delete_product(product: ProductService.delete_dep):
    return product
