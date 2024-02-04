from fastapi import FastAPI
from fastapi.exceptions import ResponseValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqlalchemy.exc import NoResultFound

from app.config import settings
from app.exceptions import sqlalchemy_not_found_exception_handler
from app.router import router


app = FastAPI(
    title="Тест проект",
    description="описание",
    version="1.0.0",
)


app.include_router(router)
app.add_exception_handler(
    NoResultFound,
    sqlalchemy_not_found_exception_handler,
)
app.add_exception_handler(
    ResponseValidationError,
    sqlalchemy_not_found_exception_handler,
)

origins = ["http://localhost:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "OPTIONS", "DELETE"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Authorization",
    ],
)


# при запуске приложения: Создается объект Redis / Инициализирует FastAPICache с бэкендом Redis и указывает префикс "cache". # noqa
# это используется для настройки кэширования с помощью Redis при старте вашего FastAPI-приложения.


@app.on_event("startup")
def startup():
    redis = aioredis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
        encoding="utf8",
        decode_response=True,
    )

    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
