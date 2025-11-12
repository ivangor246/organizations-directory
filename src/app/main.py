from fastapi import FastAPI

from app.api.root import get_root_router
from app.core.config import config


def create_app() -> FastAPI:
    app = FastAPI(
        title=config.TITLE,
        docs_url=config.DOCS_URL,
        openapi_url=config.OPENAPI_URL,
        redoc_url=config.REDOC_URL,
        debug=config.DEBUG,
    )

    root_router = get_root_router()
    app.include_router(root_router)

    return app
