import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from fastemplate.api import healthcheck, main_router
from fastemplate.api.common.errors import BaseHttpError, error_handler
from fastemplate.api.common.models import tags_metadata
from fastemplate.common.logging import setup_logging
from fastemplate.repositories.engine import Engine
from fastemplate.settings import Settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[dict[str, object]]:
    engine = Engine(settings=app.state.settings)
    app.state.engine = engine

    try:
        yield  # type: ignore[misc]
    finally:
        await engine.shutdown()


def create_app(settings: Settings) -> FastAPI:
    exception_handlers = {BaseHttpError: error_handler}
    app = FastAPI(
        title="Fastemplate",
        version=os.getenv("APP_VERSION", "dev"),
        lifespan=lifespan,
        openapi_tags=tags_metadata,
        exception_handlers=exception_handlers,  # type: ignore[arg-type]
    )
    app.state.settings = settings
    app.include_router(main_router)
    app.add_route("/hc", healthcheck, methods=["GET"], include_in_schema=False)

    return app


if __name__ == "__main__":
    settings = Settings()
    setup_logging(log_level=settings.log_level)

    app = create_app(settings)
    uvicorn.run(
        app,
        host="0.0.0.0",  # noqa: S104
        port=8000,
        log_config=None,
    )
