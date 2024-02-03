from email.message import EmailMessage

from pydantic import EmailStr

from app.config import settings


def create_register_template(email_to: EmailStr, login: str):
    email = EmailMessage()

    email["Subject"] = "Регистрация в тестовом приложении"
    email["From"] = settings.SMTP_USER
    email["To"] = email_to

    email.set_content(
        f"""
            <h1>Подтвердите регистрацию<h1>
            Вы зарегистрировались на тестовом приложении 
            Ваш логин {login} 
        """,
        subtype="html",
    )

    return email
