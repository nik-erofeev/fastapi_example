from pathlib import Path

from PIL import Image

from app.config import celery_app


@celery_app.task
def process_pic(
    path: str,
):
    # конвертирует строчку : path ="app/static/images/1.webp";
    # если оборачиваем в pwd(path), то можем обратиться path.name и получим "1.webp"
    im_path = Path(path)
    im = Image.open(im_path)

    im_resized_1000_500 = im.resize((1000, 500))
    im_resized_200_100 = im.resize((200, 100))

    im_resized_1000_500.save(f"app/static/images/res_1000_500{im_path.name}")
    im_resized_200_100.save(f"app/static/images/res_200_100{im_path.name}")
