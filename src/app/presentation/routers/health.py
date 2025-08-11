"""Health check router"""

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter

from app.config.container import Container
from app.config.settings import Settings

health_router = APIRouter(tags=["Health"])


@health_router.get("/health")
@inject
async def health_check(settings: Settings = Provide[Container.settings]) -> dict:
    """Health check endpoint"""
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "author": "eun2ce",
        "start_date": "2025-08-11",
    }
