from fastapi import APIRouter, Depends, status

from app.api.auth.utils import get_current_user
from app.api.posts.router import router as posts_router
from app.api.profiles.router import router as profile_router
from app.api.users.dependencies import check_user_permissions_dependency
from app.api.users.schemas import UserDeleteResponseSchemas, UserResponseSchemas
from app.api.users.services import UserService


router = APIRouter(
    prefix="/users",
    tags=["users"],
)
router.include_router(profile_router)
router.include_router(posts_router)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponseSchemas,
)
async def create_user(user: UserService.create_dep):
    return user


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[UserResponseSchemas],
    dependencies=[
        Depends(get_current_user),
    ],
)
async def get_many_users(user: UserService.get_many_query_dep):
    return user


@router.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserResponseSchemas,
    dependencies=[
        Depends(get_current_user),
    ],
)
async def get_user(user: UserService.get_dep):
    return user


@router.patch(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserResponseSchemas,
    dependencies=[
        Depends(get_current_user),
        Depends(check_user_permissions_dependency),
    ],
)
async def edit_user(user: UserService.edit_dep):
    return user


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserDeleteResponseSchemas,
    dependencies=[
        Depends(get_current_user),
        Depends(check_user_permissions_dependency),
    ],
)
async def delete_user(user: UserService.delete_dep):
    return user


@router.patch(
    "{user_id}/password",
    status_code=status.HTTP_200_OK,
    response_model=UserResponseSchemas,
    dependencies=[
        Depends(get_current_user),
        Depends(check_user_permissions_dependency),
    ],
)
async def change_password(user: UserService.change_password_dep):
    return user
