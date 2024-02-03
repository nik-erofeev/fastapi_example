import contextlib
from collections.abc import AsyncGenerator

from aiosmtplib import SMTP

from app.config import settings


async def connect_to_smtp_server() -> SMTP:
    """Функция для асинхронного подключения к SMTP-серверу"""

    smtp_server = SMTP(
        hostname=settings.SMTP_HOST,
        port=settings.SMTP_PORT,
        start_tls=True,
        validate_certs=False,
    )
    await smtp_server.connect()
    await smtp_server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)

    return smtp_server


async def close_smtp_connection(smtp_server: SMTP):
    """Функция для закрытия подключения к SMTP-серверу"""

    await smtp_server.quit()


async def get_smtp_connection() -> AsyncGenerator[SMTP, None]:
    """Генератор, возвращающий подключение к SMTP-серверу"""

    smtp_server = await connect_to_smtp_server()
    try:
        yield smtp_server
    except Exception as exc:
        raise exc
    finally:
        await close_smtp_connection(smtp_server)


async_smtp_session = contextlib.asynccontextmanager(get_smtp_connection)
