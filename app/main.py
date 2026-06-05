from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import get_settings
from app.core.logging import configure_logging


def create_app() -> FastAPI:
    configure_logging()
    settings = get_settings()
    application = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        description="FastAPI platform for GenAI, multi-agent workflows, and Azure data engineering.",
    )
    application.include_router(api_router, prefix=settings.api_v1_prefix)
    return application


app = create_app()
