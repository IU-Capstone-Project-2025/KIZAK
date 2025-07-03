import pytest
import logging
from faker import Faker
from unittest.mock import AsyncMock, patch
from models.user import UserResponse
from utils.logger import logger
from uuid import uuid4
from tests.conftest import FakeTransaction

logger.setLevel(logging.DEBUG)


@pytest.mark.asyncio
async def test_post_user(created_user):
    user_id = created_user["user_id"]
    assert user_id is not None


@pytest.mark.asyncio
async def test_post_invalid_user(async_client):
    faker = Faker()
    user = {
        "login": faker.email(),
        "password": faker.password()
    }
    response = await async_client.post(f"/users/", json=user)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_post_user_db_fail(async_client, fake_user_data):
    mock_conn = AsyncMock()
    mock_conn.fetchrow.return_value = None

    with patch("db.db_connector.db.transaction",
               return_value=FakeTransaction(mock_conn)):
        response = await async_client.post("/users/", json=fake_user_data)
        assert response.status_code == 500

"""
@pytest.mark.asyncio
async def test_get_user(async_client, created_user):
    response = await async_client.get(f"/users/{created_user['user_id']}")
    assert response.status_code == 200
    json_response = response.json()
    actual = UserResponse(**json_response)
    expected = UserResponse(**created_user)
    logger.debug(f"User created: {json_response}")
    logger.debug(f"User got: {json_response}")
    assert actual == expected
"""

@pytest.mark.asyncio
async def test_get_user_by_invalid_uuid(async_client):
    response = await async_client.get("/users/1")
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_update_user(async_client, created_user, fake_second_user_data):
    updated_user = fake_second_user_data
    updated_user["user_id"] = created_user["user_id"]
    response = await async_client.put("/users/", json=updated_user)
    assert response.status_code == 200
    json_response = response.json()
    logger.debug(f"User old: {created_user}")
    logger.debug(f"User new: {json_response}")
    actual = UserResponse(**json_response)
    updated_user["creation_date"] = created_user["creation_date"]
    expected = UserResponse(**updated_user)
    assert actual.model_dump() == expected.model_dump()


@pytest.mark.asyncio
async def test_update_user_by_invalid_uuid(async_client,
                                           fake_second_user_data):
    updated_user = fake_second_user_data
    updated_user["user_id"] = 1
    response = await async_client.put("/users/", json=updated_user)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_update_not_existing_user(async_client, fake_second_user_data):
    updated_user = fake_second_user_data
    updated_user["user_id"] = str(uuid4())
    response = await async_client.put(f"/users/", json=updated_user)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_clear_update_user_json(async_client, created_user):
    updated_user = {
        "user_id": created_user["user_id"]
    }
    response = await async_client.put(f"/users/", json=updated_user)
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_update_user_db_fail(async_client, fake_second_user_data,
                                   created_user):
    updated_user = fake_second_user_data
    updated_user["user_id"] = created_user["user_id"]
    mock_conn = AsyncMock()
    mock_conn.fetchrow.side_effect = [
        {"1": 1},
        None
    ]

    with patch("db.db_connector.db.transaction",
               return_value=FakeTransaction(mock_conn)):
        response = await async_client.put("/users/", json=updated_user)
        assert response.status_code == 500


@pytest.mark.asyncio
async def test_delete_user(async_client, created_user):
    response = await async_client.delete(f"/users/{created_user['user_id']}")
    assert response.status_code == 204

    response = await async_client.get(f"/users/{created_user['user_id']}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_user_by_invalid_uuid(async_client):
    response = await async_client.delete("/users/1")
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_delete_not_existing_user(async_client):
    response = await async_client.delete(f"/users/{uuid4()}")
    assert response.status_code == 404
