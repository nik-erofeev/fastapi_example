from fastapi import APIRouter, Depends, status

from app.api.auth.utils import get_current_user
from app.api.posts.schemas import PostCreateSchemas, PostResponseSchemas
from app.api.posts.services import PostService
from app.api.users.dependencies import check_user_permissions_dependency


router = APIRouter(
    prefix="/{user_id}/posts",
    tags=["posts"],
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=PostCreateSchemas,
    dependencies=[
        Depends(get_current_user),
    ],
)
async def create_profile(profile: PostService.create_dep):
    return profile


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[PostCreateSchemas],
    dependencies=[
        Depends(get_current_user),
    ],
)
async def get_many_profiles(profile: PostService.get_many_dep):
    return profile


@router.get(
    "/{profile_id}",
    status_code=status.HTTP_200_OK,
    response_model=PostResponseSchemas,
    dependencies=[
        Depends(get_current_user),
    ],
)
async def get_profile(profile: PostService.get_dep):
    return profile


@router.patch(
    "/{profile_id}",
    status_code=status.HTTP_200_OK,
    response_model=PostResponseSchemas,
    dependencies=[
        Depends(get_current_user),
        Depends(check_user_permissions_dependency),
    ],
)
async def edit_profile(profile: PostService.edit_dep):
    return profile


@router.delete(
    "/{profile_id}",
    status_code=status.HTTP_200_OK,
    response_model=PostResponseSchemas,
    dependencies=[
        Depends(get_current_user),
        Depends(check_user_permissions_dependency),
    ],
)
async def delete_profile(profile: PostService.delete_dep):
    return profile
