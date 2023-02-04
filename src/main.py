import uvicorn
from fastapi import FastAPI

from db.database import db
from metrics import metrics_instrumentator  # type: ignore
from routes import main_router
from settings import LOGGING_CONFIG, settings


def get_app() -> FastAPI:
    _app = FastAPI(
        title="Fastemplate",
        version="0.0.1",
        description="A template for FastAPI projects",
    )

    _app.include_router(main_router)
    metrics_instrumentator.instrument(_app).expose(_app, tags=["service"])

    @_app.on_event("startup")
    async def startup() -> None:
        await db.init()

    @_app.on_event("shutdown")
    async def shutdown() -> None:
        await db.close()

    return _app


def main() -> None:
    uvicorn.run(
        app="asgi:app",
        workers=settings.WORKERS,
        reload=settings.RELOAD,
        host=settings.HOST,
        port=settings.PORT,
        log_config=LOGGING_CONFIG,
        access_log=True,
    )


if __name__ == "__main__":
    main()
