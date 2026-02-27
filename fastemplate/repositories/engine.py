from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from loguru import logger
from sqlalchemy import make_url
from sqlalchemy.ext.asyncio import AsyncConnection, create_async_engine

from fastemplate.settings import Settings


class Engine:
    def __init__(self, settings: Settings) -> None:
        dsn = make_url(str(settings.postgres_dsn)).set(drivername="postgresql+psycopg")
        engine_options = {
            "echo": False,
            "pool_recycle": 3600,
            "pool_pre_ping": True,
            "connect_args": {"connect_timeout": 5, "autocommit": True},
        }
        self._engine = create_async_engine(dsn, **engine_options)
        logger.info("Engine started")

    @asynccontextmanager
    async def get_connection(self) -> AsyncIterator[AsyncConnection]:
        async with self._engine.connect() as connection:
            yield connection

    @asynccontextmanager
    async def get_transaction(self) -> AsyncIterator[AsyncConnection]:
        async with self._engine.begin() as connection:
            yield connection

    async def shutdown(self) -> None:
        await self._engine.dispose()
        logger.info("Engine shutdown")
