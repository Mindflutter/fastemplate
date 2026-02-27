import pytest
from httpx import AsyncClient
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncConnection

from fastemplate.repositories.tables import example_tbl

TEST_EXAMPLE = {"name": "test_name", "description": "test_description"}


@pytest.fixture
async def insert_example(connection: AsyncConnection) -> None:
    await connection.execute(insert(example_tbl).values(TEST_EXAMPLE))


async def test_create_example(test_client: AsyncClient, connection: AsyncConnection) -> None:
    resp = await test_client.post("/example/", json={"name": "new_name", "description": "new_desc"})
    assert resp.status_code == 201
    assert resp.json() == {"id": 1}

    res = await connection.execute(select(example_tbl.c.name, example_tbl.c.description))
    assert res.mappings().first() == {"name": "new_name", "description": "new_desc"}


async def test_create_example_no_description(test_client: AsyncClient) -> None:
    resp = await test_client.post("/example/", json={"name": "minimal"})
    assert resp.status_code == 201


@pytest.mark.usefixtures("insert_example")
async def test_create_example_duplicate(test_client: AsyncClient) -> None:
    resp = await test_client.post("/example/", json={"name": "test_name"})
    assert resp.status_code == 409


@pytest.mark.usefixtures("insert_example")
async def test_get_example(test_client: AsyncClient) -> None:
    resp = await test_client.get("/example/1")
    assert resp.status_code == 200

    data = resp.json()
    assert data["id"] == 1
    assert data["name"] == "test_name"
    assert data["description"] == "test_description"
    assert data["created_at"] is not None
    assert data["updated_at"] is not None


async def test_get_example_not_found(test_client: AsyncClient) -> None:
    resp = await test_client.get("/example/999")
    assert resp.status_code == 404
    assert resp.json() == {"message": "Example id 999 not found"}


@pytest.mark.usefixtures("insert_example")
async def test_get_examples(test_client: AsyncClient) -> None:
    resp = await test_client.get("/example/")
    assert resp.status_code == 200

    data = resp.json()
    assert data["total"] == 1
    assert len(data["items"]) == 1
    assert data["items"][0]["name"] == "test_name"


async def test_get_examples_empty(test_client: AsyncClient) -> None:
    resp = await test_client.get("/example/")
    assert resp.status_code == 200
    assert resp.json() == {"items": [], "total": 0}


@pytest.mark.usefixtures("insert_example")
async def test_update_example(test_client: AsyncClient, connection: AsyncConnection) -> None:
    resp = await test_client.put("/example/1", json={"name": "updated_name", "description": "updated_desc"})
    assert resp.status_code == 200
    assert resp.json()["name"] == "updated_name"

    res = await connection.execute(select(example_tbl.c.name).where(example_tbl.c.id == 1))
    assert res.scalar_one() == "updated_name"


async def test_update_example_not_found(test_client: AsyncClient) -> None:
    resp = await test_client.put("/example/999", json={"name": "updated"})
    assert resp.status_code == 404
    assert resp.json() == {"message": "Example id 999 not found"}


@pytest.mark.usefixtures("insert_example")
async def test_delete_example(test_client: AsyncClient, connection: AsyncConnection) -> None:
    resp = await test_client.delete("/example/1")
    assert resp.status_code == 204

    res = await connection.execute(select(example_tbl))
    assert res.first() is None


async def test_delete_example_not_found(test_client: AsyncClient) -> None:
    resp = await test_client.delete("/example/999")
    assert resp.status_code == 404
    assert resp.json() == {"message": "Example id 999 not found"}
