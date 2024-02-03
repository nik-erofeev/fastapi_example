from fastapi import APIRouter, status

from app.api.posts.schemas import PostCreateSchemas, PostResponseSchemas
from app.api.posts.services import PostService


router = APIRouter(
    prefix="/{user_id}/posts",
    tags=["posts"],
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=PostCreateSchemas,
)
async def create_profile(profile: PostService.create_dep):
    return profile


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[PostCreateSchemas],
)
async def get_many_profiles(profile: PostService.get_many_dep):
    return profile


@router.get(
    "/{profile_id}",
    status_code=status.HTTP_200_OK,
    response_model=PostResponseSchemas,
)
async def get_profile(profile: PostService.get_dep):
    return profile


@router.patch(
    "/{profile_id}",
    status_code=status.HTTP_200_OK,
    response_model=PostResponseSchemas,
)
async def edit_profile(profile: PostService.edit_dep):
    return profile


@router.delete(
    "/{profile_id}",
    status_code=status.HTTP_200_OK,
    response_model=PostResponseSchemas,
)
async def delete_profile(profile: PostService.delete_dep):
    return profile
