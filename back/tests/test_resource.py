import random
import pytest
import logging
from faker import Faker
import pytest_asyncio
from unittest.mock import AsyncMock, patch
from utils.logger import logger
from models.resource import ResourceResponse
from uuid import uuid4
from tests.conftest import FakeTransaction

logger.setLevel(logging.DEBUG)


@pytest.mark.asyncio
async def test_post_resource(created_resource):
    resource_id = created_resource["resource_id"]
    assert resource_id is not None


@pytest.mark.asyncio
async def test_post_invalid_resource(async_client):
    faker = Faker()
    resource = {
        "login": faker.email(),
        "password": faker.password()
    }
    response = await async_client.post(f"/resources/", json=resource)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_post_resource_db_fail(async_client, fake_resource_data):
    mock_conn = AsyncMock()
    mock_conn.fetchrow.return_value = None

    with patch("db.db_connector.db.transaction",
               return_value=FakeTransaction(mock_conn)):
        response = await async_client.post("/resources/",
                                           json=fake_resource_data)
        assert response.status_code == 500


@pytest.mark.asyncio
async def test_get_resource(async_client, created_resource):
    response = await async_client.get(
        f"/resources/{created_resource['resource_id']}")
    json_response = response.json()
    logger.debug(f"Resource retrieved: {json_response}")
    assert response.status_code == 200
    actual = ResourceResponse(**json_response)
    expected = ResourceResponse(**created_resource)
    assert actual == expected


@pytest.mark.asyncio
async def test_get_resource_by_invalid_uuid(async_client):
    response = await async_client.get("/resources/1")
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_update_resource(async_client, created_resource,
                               fake_second_resource_data):
    updated_resource = fake_second_resource_data
    updated_resource["resource_id"] = created_resource["resource_id"]
    response = await async_client.put("/resources/", json=updated_resource)
    json_response = response.json()
    logger.debug(f"Resource updated: {json_response}")
    assert response.status_code == 200
    actual = ResourceResponse(**json_response)
    expected = ResourceResponse(**updated_resource)
    assert actual == expected


@pytest.mark.asyncio
async def test_update_resource_by_invalid_uuid(async_client,
                                               fake_second_resource_data):
    updated_resource = fake_second_resource_data
    updated_resource["resource_id"] = 1
    response = await async_client.put("/resources/", json=updated_resource)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_update_not_existing_resource(async_client,
                                            fake_second_resource_data):
    updated_resource = fake_second_resource_data
    updated_resource["resource_id"] = str(uuid4())
    response = await async_client.put(f"/resources/", json=updated_resource)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_clear_update_resource_json(async_client, created_resource):
    updated_resource = {
        "resource_id": created_resource["resource_id"]
    }
    response = await async_client.put(f"/resources/", json=updated_resource)
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_delete_resource(async_client, created_resource):
    response = await async_client.delete(
        f"/resources/{created_resource['resource_id']}")
    assert response.status_code == 204

    response = await async_client.get(
        f"/resources/{created_resource['resource_id']}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_resource_by_invalid_uuid(async_client):
    response = await async_client.delete("/resources/1")
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_delete_not_existing_resource(async_client):
    response = await async_client.delete(f"/resources/{uuid4()}")
    assert response.status_code == 404
