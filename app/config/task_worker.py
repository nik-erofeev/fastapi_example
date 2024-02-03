# конфиг
# запуск celery: "celery -A app.config.task_worker:celery_app worker --loglevel=INFO"


from celery import Celery

from app.config import settings


celery_app = Celery(
    __name__,
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.tasks.email_and_resize_image_tasks"],
)
