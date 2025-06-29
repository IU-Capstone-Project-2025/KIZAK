import pytest
import logging
import pytest_asyncio
from utils.logger import logger

logger.setLevel(logging.DEBUG)

resource_payload = {
    "resource_type": "Course",
    "title": "Test Course",
    "summary": "Test summary",
    "content": "https://example.com/course",
    "level": "Beginner",
    "price": 0,
    "language": "English",
    "duration_hours": 3,
    "platform": "Stepik",
    "rating": 4.5,
    "published_date": "2024-06-01",
    "certificate_available": True,
    "skills_covered": ["Python", "OOP"]
}

@pytest_asyncio.fixture
async def created_resource(async_client):
    response = await async_client.post("/resources/", json=resource_payload)
    assert response.status_code == 201
    data = response.json()
    logger.debug(f"Resource created: {data}")
    return data


@pytest.mark.asyncio
async def test_create_resource(created_resource):
    assert created_resource["title"] == "Test Course"
    assert "resource_id" in created_resource


@pytest.mark.asyncio
async def test_get_resource(async_client, created_resource):
    res_id = created_resource["resource_id"]
    response = await async_client.get(f"/resource/{res_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["resource_id"] == res_id


@pytest.mark.asyncio
async def test_update_resource(async_client, created_resource):
    res_id = created_resource["resource_id"]
    update_payload = {
        "resource_id": res_id,
        "title": "Updated Title",
        "price": 10.0
    }
    response = await async_client.put("/resources/", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["price"] == 10.0


@pytest.mark.asyncio
async def test_delete_resource(async_client, created_resource):
    res_id = created_resource["resource_id"]

    response = await async_client.delete(f"/resources/{res_id}")
    assert response.status_code == 204

    response = await async_client.get(f"/resource/{res_id}")
    assert response.status_code != 200
