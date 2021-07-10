import logging

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from db import Base
from settings import settings

logger = logging.getLogger(__name__)


class Database:
    async def init(self):
        logger.info("Initializing DB")
        engine_options = {
            # verbose engine logging
            "echo": True,
            "pool_recycle": 3600,
            "pool_pre_ping": True,
            "connect_args": {"timeout": 5},
        }

        self.engine = create_async_engine(settings.DB_DSN, **engine_options)
        self.session_maker = sessionmaker(bind=self.engine, expire_on_commit=False, class_=AsyncSession)
        async with db.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def close(self):
        await self.engine.dispose()


db = Database()
