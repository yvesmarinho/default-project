from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.router import api_router
from src.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup — inicializar conexões, caches, etc.
    yield
    # shutdown — fechar conexões


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        lifespan=lifespan,
        # Desabilitar Swagger/ReDoc em produção
        docs_url=None if settings.ENV == "production" else "/docs",
        redoc_url=None if settings.ENV == "production" else "/redoc",
    )
    app.include_router(api_router, prefix="/api")
    return app


app = create_app()
