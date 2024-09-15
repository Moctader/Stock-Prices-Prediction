from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_pagination import add_pagination
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.endpoints import label_api
from app.core.settings import settings
from app.db.init_db import init_db
from app.core.logging import setup_logging


@asynccontextmanager
async def register_init(app: FastAPI):
    await init_db()
    yield


def register_app():
    app = FastAPI(
        debug=settings.DEBUG,
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description=settings.DESCRIPTION,
        docs_url=settings.DOCS_URL,
        redoc_url=settings.REDOCS_URL,
        openapi_url=settings.OPENAPI_URL,
        lifespan=register_init,
    )

    # Setup logging
    setup_logging()

    # Middleware
    register_middleware(app)

    # Routes
    register_router(app)

    # Pagination
    add_pagination(app)

    return app


def register_middleware(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def register_router(app: FastAPI):
    app.include_router(
        label_api.router,
        prefix=settings.API_PREFIX,
        tags=["label"],
    )
