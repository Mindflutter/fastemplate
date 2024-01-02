import asyncio
import logging
import sys

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from db.model_base import Base
from settings import settings

logger = logging.getLogger(__name__)


class Database:
    def __init__(self, engine: AsyncEngine, session_maker: async_sessionmaker):
        self.engine = engine
        self.session_maker = session_maker

    async def init(self) -> None:
        logger.info("Initializing DB")
        await self.wait_for_connection()

        # the DB schema and tables already exist in a real service, so this is here for convenience only
        async with db.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def wait_for_connection(self) -> None:
        """DB connection exponential backoff method."""
        tries = 0
        while tries < settings.DB_CONN_TRIES:
            try:
                async with self.engine.begin():
                    # return immediately on connection success
                    return
            except OSError:
                logger.info("Waiting for DB connection...")
                await asyncio.sleep(2**tries)
                tries += 1

        logger.error("Awaited DB connection for too long, shutting down")
        sys.exit("DB connection timeout")

    async def close(self) -> None:
        if self.engine:
            await self.engine.dispose()


engine_options = {
    # logging configured via settings
    "echo": False,
    "pool_recycle": 3600,
    "pool_pre_ping": True,
    "connect_args": {"connect_timeout": 5},
}
db_engine = create_async_engine(settings.DB_DSN, **engine_options)
db_session_maker = async_sessionmaker(bind=db_engine, expire_on_commit=False, class_=AsyncSession)

db = Database(db_engine, db_session_maker)
