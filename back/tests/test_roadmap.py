import pytest
import pytest_asyncio
from models.roadmap import RoadmapResponse, RoadmapInfo
from utils.logger import logger
from unittest.mock import AsyncMock, patch
from uuid import uuid4
from tests.conftest import FakeTransaction


@pytest.mark.asyncio
async def test_post_roadmap(created_roadmap):
    roadmap_id = created_roadmap["roadmap_id"]
    assert roadmap_id is not None


@pytest.mark.asyncio
async def test_post_invalid_roadmap(async_client):
    response = await async_client.post(f"/roadmap/", json={})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_post_roadmap_db_fail(async_client, created_user):
    mock_conn = AsyncMock()
    mock_conn.fetchrow.return_value = None

    with patch("db.db_connector.db.transaction",
               return_value=FakeTransaction(mock_conn)):
        response = await async_client.post("/roadmap/", json={
            "user_id": created_user["user_id"]})
        assert response.status_code == 500


@pytest.mark.asyncio
async def test_get_roadmap(async_client, created_roadmap):
    response = await async_client.get(
        f"/roadmap/{created_roadmap['roadmap_id']}")
    assert response.status_code == 200
    json_response = response.json()
    logger.debug(f"Roadmap response: {json_response}")
    actual = RoadmapInfo(**json_response)
    expected_json = {
        "roadmap_id": created_roadmap["roadmap_id"],
        "links": [],
        "nodes": []
    }
    expected = RoadmapInfo(**expected_json)
    assert actual == expected


@pytest.mark.asyncio
async def test_get_roadmap_by_invalid_uuid(async_client):
    response = await async_client.get("/roadmap/1")
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_delete_roadmap(async_client, created_roadmap):
    response = await async_client.delete(
        f"/roadmap/{created_roadmap['roadmap_id']}")
    assert response.status_code == 204

    logger.debug("Roadmap deleted")

    response = await async_client.get(
        f"/roadmap/{created_roadmap['roadmap_id']}")

    logger.debug(f"Roadmap response: {response.json()}")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_roadmap_by_invalid_uuid(async_client):
    response = await async_client.delete("/roadmap/1")
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_delete_not_existing_roadmap(async_client):
    response = await async_client.delete(f"/roadmap/{uuid4()}")
    assert response.status_code == 404
