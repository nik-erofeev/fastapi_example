import time
from random import randint, random

from fastapi import APIRouter


service_router = login_router = APIRouter(
    prefix="/sentry_prometheus",
    tags=["Sentry + Grafana + Prometheus"],
)


@service_router.get("/ping")
async def ping():
    if randint(0, 10) % 2 == 0:
        raise ValueError
    raise ZeroDivisionError
    return {"Success": True}


@service_router.get("/get_error")
def get_error():
    if random() > 0.5:
        raise ZeroDivisionError
    else:
        raise KeyError


@service_router.get("/time_consumer")
def time_consumer():
    time.sleep(random() * 5)
    return 1


@service_router.get("/memory_consumer")
def memory_consumer():
    _ = [i for i in range(10_000_000)]
    return 1
