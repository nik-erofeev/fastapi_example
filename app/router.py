"""Корневой роутер приложения"""

from fastapi import APIRouter

from app.api.admin_roles.router import router as roles_router
from app.api.auth.router import router as auth_router
from app.api.images.router import router as images_router
from app.api.products.router import router as products_router
from app.api.sentry_prometheus.router import service_router as sentry_router
from app.api.users.router import router as user_router
from app.config import settings


router = APIRouter(prefix=settings.api_v1_prefix)

routers = (
    user_router,
    auth_router,
    products_router,
    images_router,
    roles_router,
    sentry_router,
)


for resource_router in routers:
    router.include_router(resource_router)
