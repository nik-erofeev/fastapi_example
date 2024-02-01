from fastapi import APIRouter, status


router = APIRouter(prefix="/users", tags=["user"])


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_users():
    return {"users": "ok"}
