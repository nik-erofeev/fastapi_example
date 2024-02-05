from email.message import EmailMessage

from app.config import settings


def create_register_template(email_to: str, login: str, password: str):
    email = EmailMessage()

    email["Subject"] = "Регистрация в тестовом приложении"
    email["From"] = settings.SMTP_USER
    email["To"] = email_to

    body = (
        f"Регистрация в системе\n"
        f"Вас добавили в систему\n"
        f"Данные для входа:\n"
        f"Логин: {login}\n"
        f"Пароль: {password}"
    )

    email.set_content(body, subtype="plain")

    return email
