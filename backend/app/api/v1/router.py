from fastapi import APIRouter

from app.api.v1.health import router as health_router
from app.api.v1.corridas import router as corridas_router

api_router = APIRouter()
api_router.include_router(health_router, tags=["health"])
api_router.include_router(corridas_router, tags=["corridas"])