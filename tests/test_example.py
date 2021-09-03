import pytest
from httpx import AsyncClient

from asgi import app

pytestmark = [pytest.mark.usefixtures("db_tables", "db_app", "db_data"), pytest.mark.asyncio]


async def test_get():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/example/1")
    assert response.status_code == 200
    assert response.json() == {"description": "description", "id": 1, "name": "test"}


async def test_validation_error():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/example/WRONG")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [{"loc": ["path", "example_id"], "msg": "value is not a valid integer", "type": "type_error.integer"}]
    }


async def test_not_found():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/example/2")
    assert response.status_code == 404
    assert response.json() == {"message": "Example id 2 not found"}


async def test_create():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/example/", json={"name": "new_name"})
    assert response.status_code == 201
    assert response.json() == {"example_id": 2}


async def test_duplicate_name():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/example/", json={"name": "test"})
    assert response.status_code == 409
    assert response.json() == {"message": "Name test already exists"}


async def test_update():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.put("/example/1", json={"name": "updated_name"})
    assert response.status_code == 200


async def test_update_not_found():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.put("/example/2", json={"name": "updated_name"})
    assert response.status_code == 404
    assert response.json() == {"message": "Example id 2 not found"}


async def test_delete():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.delete("/example/1")
    assert response.status_code == 200


async def test_delete_not_found():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.delete("/example/2")
    assert response.status_code == 404
    assert response.json() == {"message": "Example id 2 not found"}
