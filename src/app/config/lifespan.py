"""Application lifespan management"""

from contextlib import asynccontextmanager

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""

    print("Starting up llmplan...")

    container = app.state.container
    container.wire(
        modules=container.wiring_config.modules,
        packages=container.wiring_config.packages,
    )

    yield

    print("Shutting down llmplan...")
    container.unwire()
