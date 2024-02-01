"""Корневой роутер приложения"""

from fastapi import APIRouter

from app.api.users.router import router as user_router


router = APIRouter(prefix="/api/v1")

routers = (user_router,)


for resource_router in routers:
    router.include_router(resource_router)
