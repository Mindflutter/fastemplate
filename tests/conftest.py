from collections.abc import AsyncIterator, Iterator

import pytest
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx2 import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncConnection
from testcontainers.postgres import PostgresContainer

from fastemplate.app import create_app
from fastemplate.repositories.engine import Engine
from fastemplate.repositories.tables import metadata
from fastemplate.settings import Settings


@pytest.fixture(scope="session")
def postgres_dsn() -> Iterator[str]:
    with PostgresContainer("postgres:18-alpine", driver="psycopg") as container:
        yield container.get_connection_url()


@pytest.fixture(scope="session")
def settings(postgres_dsn: str) -> Settings:
    return Settings(postgres_dsn=postgres_dsn)


@pytest.fixture(scope="session")
async def test_app(settings: Settings) -> AsyncIterator[FastAPI]:
    app = create_app(settings)
    async with LifespanManager(app):
        yield app


@pytest.fixture(scope="session")
async def test_client(test_app: FastAPI) -> AsyncIterator[AsyncClient]:
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.fixture(scope="session")
def engine(test_app: FastAPI) -> Engine:
    return test_app.state.engine


@pytest.fixture(scope="session")
async def connection(engine: Engine) -> AsyncIterator[AsyncConnection]:
    async with engine.get_connection() as conn:
        yield conn


@pytest.fixture(scope="session", autouse=True)
async def create_tables(engine: Engine) -> None:
    """Create all tables once before any tests run."""
    async with engine.get_connection() as conn:
        await conn.run_sync(metadata.create_all)


@pytest.fixture(autouse=True)
async def db_cleanup(connection: AsyncConnection) -> AsyncIterator[None]:
    """Truncate all tables after each test."""
    yield
    await connection.execute(text("TRUNCATE example RESTART IDENTITY CASCADE"))
