# pylint: disable=redefined-outer-name
import asyncio

import pytest
import pytest_asyncio
from sqlalchemy import text

from alembic import config
from alembic.command import downgrade, upgrade
from db import Example
from db.database import db
from db.model_base import Base
from settings import PROJECT_ROOT, settings


@pytest.fixture(scope="session")
def alembic_config():
    config_path = PROJECT_ROOT / "alembic.ini"
    alembic_config = config.Config(config_path)
    alembic_config.set_main_option("sqlalchemy.url", settings.DB_DSN)
    return alembic_config


@pytest.fixture(scope="session")
def db_tables(alembic_config):
    """A fixture for creating / dropping all tables in an empty DB.

    Up for entire test session
    """
    upgrade(alembic_config, "head")
    yield
    downgrade(alembic_config, "base")


@pytest_asyncio.fixture(scope="session")
async def db_app():
    """A fixture for initializing app DB object for the entire test session."""
    await db.init()
    yield
    await db.close()


@pytest.fixture(scope="session")
def event_loop():
    """A fixture for overriding pytest.asyncio event loop.

    One event loop is used by all tests.
    """
    return asyncio.get_event_loop()


@pytest_asyncio.fixture
async def db_data():
    """A fixture for populating test DB with test data.

    Test data is truncated at the end of each test.
    """
    async with db.session_maker() as session:
        example = Example(name="test", description="description")
        session.add(example)
        await session.commit()

    yield

    async with db.session_maker() as session:
        for table in Base.metadata.sorted_tables:
            await session.execute(text(f"TRUNCATE {table} RESTART IDENTITY CASCADE"))
            await session.commit()
