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
async def get_all(product: ProductService.get_many_dep):
    return product


@router.get(
    "/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=ProductResponseSchemas,
)
async def get(product: ProductService.get_dep):
    return product


@router.patch(
    "/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=ProductResponseSchemas,
)
async def patch(product: ProductService.edit_dep):
    return product


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=ProductResponseSchemas,
)
async def delete(product: ProductService.delete_dep):
    return product
