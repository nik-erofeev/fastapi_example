from email.mime.text import MIMEText

from app.config import settings
from app.notifications.base_notification import BaseNotification
from app.notifications.utils import async_smtp_session


class EmailNotification(BaseNotification):
    """Класс для отправки уведомлений по email"""

    @staticmethod
    def _create_message(
        body: str,
        header: str,
        receivers: list[str],
    ) -> str:
        """Создание сообщения для отправки по email"""

        msg = MIMEText(body)
        msg["Subject"] = header
        msg["From"] = settings.SMTP_USER
        msg["To"] = ",".join(receivers)

        return msg.as_string()

    async def send_notification(
        self,
        body: str,
        header: str,
        receivers: list[str],
    ):
        """Отправка сообщений по email"""

        async with async_smtp_session() as session:
            email = self._create_message(body, header, receivers)
            await session.sendmail(settings.SMTP_USER, receivers, email)


email_notification = EmailNotification()
