from fastapi import APIRouter, Depends, File, status

from app.api.images.services import save_images


router = APIRouter(
    prefix="/images",
    tags=["Загрузка картинок"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def upload_images(image: File = Depends(save_images)):
    return image.filename
