import uvicorn
from fastapi import FastAPI

from routes import main_router
from settings import LOGGING_CONFIG, settings


def get_app():
    _app = FastAPI(
        title="Fastemplate",
        version="0.0.1",
        description="A template for FastAPI projects",
    )

    _app.include_router(main_router)

    @_app.on_event("startup")
    async def startup():
        pass

    @_app.on_event("shutdown")
    async def shutdown():
        pass

    return _app


if __name__ == "__main__":
    uvicorn.run(
        app="asgi:app",
        workers=settings.WORKERS,
        reload=settings.RELOAD,
        host=settings.HOST,
        port=settings.PORT,
        log_config=LOGGING_CONFIG,
        access_log=True,
    )
