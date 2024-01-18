from typing import Annotated, List
from fastapi import Depends, APIRouter
from fastapi import BackgroundTasks
import time

from service.logging_handler import get_uvicorn_logger

main_router = APIRouter(
    tags=["Scoring Algorithm"],
    responses={
        500: {"description": "Internal Server Error"},
        404: {"description": "Not Found"},
    },
)


@main_router.get("/status")
async def status():
    pass


# k8s liveness probe
@main_router.get("/liveness/", status_code=200)
async def liveness_check():
    return "Liveness check succeeded."

