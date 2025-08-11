"""
FastAPI Application Entry Point
"""

from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from app.config.container import Container
from app.config.lifespan import lifespan
from app.presentation.routers import summary
from app.presentation.routers.health import health_router

container = Container()


def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    settings = container.settings.provided()

    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
        Middleware(GZipMiddleware),
    ]

    app = FastAPI(
        title="llmplan",
        description="",
        version="0.1.0",
        middleware=middleware,
        lifespan=lifespan,
    )

    app.state.container = container
    app.state.settings = settings

    app.include_router(health_router, prefix="/api/v1")
    app.include_router(summary.router, prefix="/api/v1")

    return app


app = create_app()
