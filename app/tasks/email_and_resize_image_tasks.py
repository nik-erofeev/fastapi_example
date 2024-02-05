import smtplib
from pathlib import Path

from PIL import Image

from app.config import celery_app, settings
from app.tasks.email_templates import create_register_template


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


@celery_app.task(name="send_email_registration")
def send_confirmation_of_registration_email_flower(
    email_to: str,
    login: str,
    password: str,
):
    # Todo заменить  email_to_mock на email_to !!!!
    # заменили чтобы самому себе отправить для теста
    email_to_mock = settings.SMTP_USER

    msg_content = create_register_template(email_to_mock, login, password)

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)

        server.send_message(msg_content)
