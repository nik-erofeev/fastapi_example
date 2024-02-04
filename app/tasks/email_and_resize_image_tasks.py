from pathlib import Path

from PIL import Image
from pydantic import EmailStr

from app.config import celery_app, settings
from app.notifications.email_notification import email_notification
from app.notifications.templates import send_password_template


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


@celery_app.task(name="send_password_registration")
async def send_confirmation_of_registration_email(
    email_to: EmailStr,
    login: str,
    password: str,
):
    # Todo замениnm email_to - email_to_mock
    # заменили чтобы самому себе отправить для теста
    email_to_mock = settings.SMTP_USER
    #
    msg_content = send_password_template(login=login, password=password)

    await email_notification.send_notification(
        body=msg_content["body"],
        header=msg_content["header"],
        receivers=[email_to_mock],
    )
