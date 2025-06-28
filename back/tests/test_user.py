import pytest
import logging
from faker import Faker
from fastapi.testclient import TestClient
from models.user import UserCreate, UserResponse, UserUpdate
from app import app
from utils.logger import logger
import time

logger.setLevel(logging.DEBUG)
client = TestClient(app)


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


@pytest.fixture
def created_user(fake_user_data):
    time.sleep(1)
    response = client.post("/users/", json=fake_user_data)
    json_response = response.json()
    logger.debug(f"User created: {json_response}")
    assert response.status_code == 201
    UserResponse(**json_response)
    return json_response


def test_post_user(created_user):
    user_id = created_user["user_id"]
    assert user_id is not None


def test_get_user(created_user, fake_user_data):
    response = client.get(f"/users/{created_user['user_id']}")
    json_response = response.json()
    UserResponse(**json_response)
    assert response.status_code == 200
    assert json_response == created_user


def test_update_user(fake_user_data, created_user):
    updated_user = fake_user_data
    updated_user["user_id"] = created_user["user_id"]
    response = client.put(f"/users/", json=updated_user)
    json_response = response.json()
    UserResponse(**json_response)
    assert response.status_code == 200
    assert json_response == created_user


def test_delete_user(created_user):
    response = client.delete(f"/users/{created_user['user_id']}")
    assert response.status_code == 204
    response = client.get(f"/users/{created_user['user_id']}")
    assert response.status_code == 404
