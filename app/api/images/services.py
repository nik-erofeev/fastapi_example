import shutil

from fastapi import File, UploadFile

from app.tasks.resize_image_tasks import process_pic


async def save_images(file: UploadFile = File(...)):
    im_path = f"app/static/images/{file.filename.split('.')[0]}.webp"
    with open(im_path, "wb") as file_obj:
        shutil.copyfileobj(file.file, file_obj)

    process_pic.delay(im_path)

    return {"фото загружено": file.filename}
