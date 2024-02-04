from fastapi import FastAPI
from fastapi.exceptions import ResponseValidationError
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import NoResultFound

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
