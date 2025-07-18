# tests/conftest.py
import pytest
import random
import pytest_asyncio
from httpx import AsyncClient
from faker import Faker
from app import app
from db.db_connector import db
from models.user import UserResponse
from models.roadmap import RoadmapResponse, NodeResponse, LinkResponse
from models.resource import ResourceResponse
from utils.logger import logger
import os

os.environ.setdefault("SECRET_KEY", "test-secret-key")
os.environ.setdefault("JWT_SECRET_KEY", "test-secret-key")
os.environ.setdefault("PASSWORD_SALT", "test-salt")


class FakeTransaction:
    def __init__(self, conn):
        self.conn = conn

    async def __aenter__(self):
        return self.conn

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass


@pytest_asyncio.fixture(scope="function")
async def setup_db():
    await db.connect()
    yield
    await db.close()


@pytest_asyncio.fixture
async def async_client(setup_db):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


def generate_fake_user_data():
    faker = Faker()
    return {
        "mail": faker.email(),
        "login": faker.email(),
        "password": faker.password(),
        "background": faker.sentence(),
        "education": faker.sentence(),
        "goals": faker.sentence(),
        "goal_vacancy": faker.job(),
        "skills": [
            {
                "is_goal": random.choice(["true", "false"]),
                "skill": faker.word(),
                "skill_level": random.choice(
                    ['Beginner', 'Intermediate', 'Advanced']),
            },
            {
                "is_goal": random.choice(["true", "false"]),
                "skill": faker.word(),
                "skill_level": random.choice(
                    ['Beginner', 'Intermediate', 'Advanced']),
            }
        ]
    }


@pytest.fixture
def fake_user_data():
    return generate_fake_user_data()


@pytest.fixture
def fake_second_user_data():
    return generate_fake_user_data()


@pytest_asyncio.fixture
async def created_user(async_client, fake_user_data):
    response = await async_client.post("/users/", json=fake_user_data)
    json_response = response.json()
    logger.debug(f"User created: {json_response}")
    assert response.status_code == 201
    UserResponse(**json_response)
    return json_response


@pytest_asyncio.fixture
async def created_roadmap(async_client, created_user):
    response = await async_client.post("/roadmap/", json={
        "user_id": created_user["user_id"]})
    json_response = response.json()
    assert response.status_code == 201
    RoadmapResponse(**json_response)
    return json_response



def generate_fake_resource_data():
    faker = Faker()
    return {
        "resource_type": random.choice(["Course", "Article"]),
        "title": faker.sentence(),
        "summary": faker.sentence(),
        "content": faker.url(),
        "level": random.choice(
            ['Beginner', 'Intermediate', 'Advanced', 'All Levels']),
        "price": faker.random_int(),
        "language": faker.language_name(),
        "duration_hours": faker.random_int(),
        "platform": faker.company(),
        "rating": faker.random_int(0, 5),
        "published_date": faker.date(),
        "certificate_available": random.choice(["true", "false"]),
        "skills_covered": [
            faker.word(),
            faker.word()
        ]
    }


@pytest.fixture
def fake_resource_data():
    return generate_fake_resource_data()


@pytest.fixture
def fake_second_resource_data():
    return generate_fake_resource_data()


@pytest_asyncio.fixture
async def created_resource(async_client, fake_resource_data):
    response = await async_client.post("/resources/", json=fake_resource_data)
    json_response = response.json()
    logger.debug(f"Resource created: {json_response}")
    assert response.status_code == 201
    ResourceResponse(**json_response)
    return json_response


def generate_fake_node_data():
    faker = Faker()
    return {
        "title": faker.sentence(),
        "summary": faker.sentence(),
        "progress": random.choice(["Not started", "In progress", "Done"])
    }


@pytest.fixture
def fake_node_data():
    return generate_fake_node_data()


@pytest.fixture
def fake_second_node_data():
    return generate_fake_node_data()


@pytest_asyncio.fixture
async def created_node(async_client, fake_node_data, created_roadmap,
                       created_resource):
    fake_node_data["roadmap_id"] = created_roadmap["roadmap_id"]
    fake_node_data["resource_id"] = created_resource["resource_id"]
    response = await async_client.post("/node/", json=fake_node_data)
    json_response = response.json()
    assert response.status_code == 201
    NodeResponse(**json_response)
    return json_response


@pytest_asyncio.fixture
async def created_two_nodes(async_client, fake_node_data,
                            fake_second_node_data,
                            created_roadmap,
                            created_resource):
    fake_second_node_data["roadmap_id"] = created_roadmap[
        "roadmap_id"]
    fake_second_node_data["resource_id"] = created_resource[
        "resource_id"]
    fake_node_data["roadmap_id"] = created_roadmap[
        "roadmap_id"]
    fake_node_data["resource_id"] = created_resource[
        "resource_id"]
    response1 = await async_client.post("/node/",
                                        json=fake_node_data)
    response2 = await async_client.post("/node/",
                                        json=fake_second_node_data)
    json_response1 = response1.json()
    assert response1.status_code == 201
    json_response2 = response2.json()
    assert response2.status_code == 201
    NodeResponse(**json_response1)
    NodeResponse(**json_response2)
    return json_response1, json_response2


@pytest_asyncio.fixture
async def created_link(async_client, created_roadmap,
                       created_two_nodes):
    node_from, node_to = created_two_nodes
    link = {
        "roadmap_id": created_roadmap["roadmap_id"],
        "from_node": node_from["node_id"],
        "to_node": node_to["node_id"]
    }
    response = await async_client.post("/link/", json=link)
    json_response = response.json()
    assert response.status_code == 201
    LinkResponse(**json_response)
    return json_response
