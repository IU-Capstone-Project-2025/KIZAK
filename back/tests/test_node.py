import pytest
import pytest_asyncio
from faker import Faker
from models.roadmap import NodeResponse
from unittest.mock import AsyncMock, patch
from uuid import uuid4
from tests.conftest import FakeTransaction


@pytest.mark.asyncio
async def test_post_node(created_node):
    node_id = created_node["node_id"]
    assert node_id is not None


@pytest.mark.asyncio
async def test_post_invalid_node(async_client):
    faker = Faker()
    node = {
        "title": faker.sentence(),
    }
    response = await async_client.post(f"/node/", json=node)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_post_node_db_fail(async_client, fake_node_data, created_roadmap,
                                 created_resource):
    mock_conn = AsyncMock()
    mock_conn.fetchrow.return_value = None

    fake_node_data["roadmap_id"] = created_roadmap["roadmap_id"]
    fake_node_data["resource_id"] = created_resource["resource_id"]

    with patch("db.db_connector.db.transaction",
               return_value=FakeTransaction(mock_conn)):
        response = await async_client.post("/node/", json=fake_node_data)
        assert response.status_code == 500


@pytest.mark.asyncio
async def test_get_node(async_client, created_node):
    response = await async_client.get(f"/node/{created_node['node_id']}")
    assert response.status_code == 200
    json_response = response.json()
    actual = NodeResponse(**json_response)
    expected = NodeResponse(**created_node)
    assert actual == expected


@pytest.mark.asyncio
async def test_get_node_by_invalid_uuid(async_client):
    response = await async_client.get("/node/1")
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_update_node(async_client, created_node, fake_second_node_data,
                           created_resource, created_roadmap):
    updated_node = fake_second_node_data
    updated_node["node_id"] = created_node["node_id"]
    response = await async_client.put("/node/", json=updated_node)
    assert response.status_code == 200
    json_response = response.json()
    actual = NodeResponse(**json_response)
    updated_node["roadmap_id"] = created_roadmap["roadmap_id"]
    updated_node["resource_id"] = created_resource["resource_id"]
    expected = NodeResponse(**updated_node)
    assert actual == expected


@pytest.mark.asyncio
async def test_update_node_by_invalid_uuid(async_client,
                                           fake_second_node_data):
    updated_node = fake_second_node_data
    updated_node["node_id"] = 1
    response = await async_client.put("/node/", json=updated_node)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_update_not_existing_node(async_client, fake_second_node_data):
    updated_node = fake_second_node_data
    updated_node["node_id"] = str(uuid4())
    response = await async_client.put(f"/node/", json=updated_node)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_clear_update_node_json(async_client, created_node):
    updated_node = {
        "node_id": created_node["node_id"]
    }
    response = await async_client.put(f"/node/", json=updated_node)
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_delete_node(async_client, created_node):
    response = await async_client.delete(f"/node/{created_node['node_id']}")
    assert response.status_code == 204

    response = await async_client.get(f"/node/{created_node['node_id']}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_node_by_invalid_uuid(async_client):
    response = await async_client.delete("/node/1")
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_delete_not_existing_node(async_client):
    response = await async_client.delete(f"/node/{uuid4()}")
    assert response.status_code == 404
