from fastapi import APIRouter, status

from app.api.profiles.schemas import ProfileResponseSchemas
from app.api.profiles.services import ProfileService


router = APIRouter(
    prefix="/{user_id}/profile",
    tags=["profile"],
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ProfileResponseSchemas,
)
async def create_profile(profile: ProfileService.create_dep):
    return profile


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[ProfileResponseSchemas],
)
async def get_many_profiles(profile: ProfileService.get_many_dep):
    return profile


@router.get(
    "/{profile_id}",
    status_code=status.HTTP_200_OK,
    response_model=ProfileResponseSchemas,
)
async def get_profile(profile: ProfileService.get_dep):
    return profile


@router.patch(
    "/{profile_id}",
    status_code=status.HTTP_200_OK,
    response_model=ProfileResponseSchemas,
)
async def edit_profile(profile: ProfileService.edit_dep):
    return profile


@router.delete(
    "/{profile_id}",
    status_code=status.HTTP_200_OK,
    response_model=ProfileResponseSchemas,
)
async def delete_profile(profile: ProfileService.delete_dep):
    return profile
