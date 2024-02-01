from dotenv import load_dotenv
from pydantic_settings import BaseSettings


load_dotenv()


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"
    SERVER_HOST: str = "127.0.0.1"
    SERVER_PORT: int = 8000
    DEBUG: bool = True

    DATABASE_USER: str | None = None
    DATABASE_PASSWORD: str | None = None
    DATABASE_HOST: str | None = None
    DATABASE_PORT: str | None = None
    DATABASE_NAME: str | None = None

    DATABASE_USER_TEST: str | None = None
    DATABASE_PASSWORD_TEST: str | None = None
    DATABASE_HOST_TEST: str | None = None
    DATABASE_PORT_TEST: str | None = None
    DATABASE_NAME_TEST: str | None = None

    JWT_SECRET_KEY: str
    REFRESH_SECRET_KEY: str
    ALGORITHM: str
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    CELERY_BROKER_URL: str = "redis://localhost:6379"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379"

    REDIS_HOST: str
    REDIS_PORT: int

    SMTP_HOST: str | None = None
    SMTP_PORT: int | None = None
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None

    @property
    def database_url(self) -> str:
        if not all(
            (
                self.DATABASE_USER,
                self.DATABASE_PASSWORD,
                self.DATABASE_HOST,
                self.DATABASE_PORT,
                self.DATABASE_NAME,
            ),
        ):
            raise ValueError(
                "Отсутствуют необходимые данные для подключения к БД",
            )

        return (
            f"postgresql+asyncpg://"
            f"{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@"
            f"{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
        )

    @property
    def database_url_test(self) -> str:
        if not all(
            (
                self.DATABASE_USER_TEST,
                self.DATABASE_PASSWORD_TEST,
                self.DATABASE_HOST_TEST,
                self.DATABASE_PORT_TEST,
                self.DATABASE_NAME_TEST,
            ),
        ):
            raise ValueError(
                "Отсутствуют необходимые данные для подключения к БД",
            )

        return (
            f"postgresql+asyncpg://"
            f"{self.DATABASE_USER_TEST}:{self.DATABASE_PASSWORD_TEST}@"
            f"{self.DATABASE_HOST_TEST}:{self.DATABASE_PORT_TEST}/{self.DATABASE_NAME_TEST}"
        )

    # class Config:
    #     env_file = "../.env"


settings = Settings(
    _env_file=".env",
    _env_file_encoding="utf-8",
)
