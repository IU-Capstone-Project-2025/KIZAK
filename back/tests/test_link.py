import pytest
import pytest_asyncio
import logging
from faker import Faker
from unittest.mock import AsyncMock, patch
from models.roadmap import LinkResponse
from utils.logger import logger
from uuid import uuid4
from tests.conftest import FakeTransaction


@pytest.mark.asyncio
async def test_post_link(created_link):
    link_id = created_link["link_id"]
    assert link_id is not None


@pytest.mark.asyncio
async def test_post_invalid_link(async_client):
    faker = Faker()
    link = {
        "roadmap_id": str(faker.uuid4()),
    }
    response = await async_client.post(f"/link/", json=link)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_post_link_db_fail(async_client, created_roadmap,
                                 created_two_nodes):
    mock_conn = AsyncMock()
    mock_conn.fetchrow.return_value = None

    node_from, node_to = created_two_nodes
    link = {
        "roadmap_id": created_roadmap["roadmap_id"],
        "from_node": node_from["node_id"],
        "to_node": node_to["node_id"]
    }

    with patch("db.db_connector.db.transaction",
               return_value=FakeTransaction(mock_conn)):
        response = await async_client.post("/link/", json=link)
        assert response.status_code == 500


@pytest.mark.asyncio
async def test_get_link(async_client, created_link):
    response = await async_client.get(f"/link/{created_link['link_id']}")
    assert response.status_code == 200
    json_response = response.json()
    actual = LinkResponse(**json_response)
    expected = LinkResponse(**created_link)
    assert actual == expected


@pytest.mark.asyncio
async def test_get_link_by_invalid_uuid(async_client):
    response = await async_client.get("/link/1")
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_delete_link(async_client, created_link):
    response = await async_client.delete(f"/link/{created_link['link_id']}")
    assert response.status_code == 204

    response = await async_client.get(f"/link/{created_link['link_id']}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_link_by_invalid_uuid(async_client):
    response = await async_client.delete("/link/1")
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_delete_not_existing_link(async_client):
    response = await async_client.delete(f"/link/{uuid4()}")
    assert response.status_code == 404
