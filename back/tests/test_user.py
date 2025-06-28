import pytest
import pytest_asyncio
import logging
from faker import Faker
from httpx import AsyncClient
from models.user import UserCreate, UserResponse, UserUpdate
from app import app
from utils.logger import logger

logger.setLevel(logging.DEBUG)


@pytest.fixture
def fake_user_data():
    faker = Faker()
    return {
        "login": faker.email(),
        "password": faker.password(),
        "background": faker.sentence(),
        "education": faker.sentence(),
        "goals": faker.sentence(),
        "goal_vacancy": faker.job(),
        "skills": [
            {
                "is_goal": False,
                "skill": "Python",
                "skill_level": "Intermediate"
            },
            {
                "is_goal": True,
                "skill": "Machine Learning",
                "skill_level": "Beginner"
            }
        ]
    }


@pytest_asyncio.fixture
async def created_user(fake_user_data):
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/users/", json=fake_user_data)
        json_response = await response.json()
        logger.debug(f"User created: {json_response}")
        UserResponse(**json_response)
        assert response.status_code == 201
        return json_response

async def test_post_user(created_user):
    user_id = created_user["user_id"]
    assert user_id is not None


@pytest.mark.asyncio
async def test_get_user(created_user, fake_user_data):
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get(f"/users/{created_user['user_id']}")
        json_response = await response.json()
        UserResponse(**json_response)
        assert response.status_code == 200
        assert json_response == created_user


@pytest.mark.asyncio
async def test_update_user(fake_user_data, created_user):
    async with AsyncClient(app=app, base_url="http://test") as client:
        updated_user = fake_user_data
        updated_user["user_id"] = created_user["user_id"]
        response = await client.put(f"/users/", json=updated_user)
        json_response = await response.json()
        UserResponse(**json_response)
        assert response.status_code == 200
        assert json_response == created_user


@pytest.mark.asyncio
async def test_delete_user(created_user):
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.delete(f"/users/{created_user['user_id']}")
        assert response.status_code == 204
        response = await client.get(f"/users/{created_user['user_id']}")
        assert response.status_code == 404
