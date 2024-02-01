from fastapi import APIRouter, status

from app.api.users.schemas import UserResponseSchemas
from app.api.users.services import UserService


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponseSchemas,
)
async def create(user: UserService.create_dep):
    return user


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[UserResponseSchemas],
    # dependencies=[Depends(get_current_user)],
)
async def get_all(user: UserService.get_many_dep):
    return user


@router.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserResponseSchemas,
)
async def get(user: UserService.get_dep):
    return user


@router.patch(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserResponseSchemas,
)
async def patch(user: UserService.edit_dep):
    return user


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserResponseSchemas,
)
async def delete(user: UserService.delete_dep):
    return user


@router.patch(
    "{user_id}/password",
    status_code=status.HTTP_200_OK,
    response_model=UserResponseSchemas,
)
async def change_password(user: UserService.change_password_dep):
    return user
