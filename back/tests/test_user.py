import pytest
import pytest_asyncio
import logging
from faker import Faker
from models.user import UserResponse
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
async def created_user(async_client, fake_user_data):
    response = await async_client.post("/users/", json=fake_user_data)
    assert response.status_code == 201
    json_response = response.json()
    logger.debug(f"User created: {json_response}")
    UserResponse(**json_response)  # validate schema
    return json_response


@pytest.mark.asyncio
async def test_post_user(created_user):
    user_id = created_user["user_id"]
    assert user_id is not None


@pytest.mark.asyncio
async def test_get_user(async_client, created_user):
    response = await async_client.get(f"/users/{created_user['user_id']}")
    assert response.status_code == 200
    json_response = response.json()
    UserResponse(**json_response)
    assert json_response == created_user


@pytest.mark.asyncio
async def test_update_user(async_client, created_user, fake_user_data):
    updated_user = fake_user_data.copy()
    updated_user["user_id"] = created_user["user_id"]
    response = await async_client.put("/users/", json=updated_user)
    assert response.status_code == 200
    json_response = response.json()
    UserResponse(**json_response)
    assert json_response == created_user


@pytest.mark.asyncio
async def test_delete_user(async_client, created_user):
    response = await async_client.delete(f"/users/{created_user['user_id']}")
    assert response.status_code == 204

    response = await async_client.get(f"/users/{created_user['user_id']}")
    assert response.status_code == 404
