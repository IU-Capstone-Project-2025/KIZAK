# tests/conftest.py
import pytest_asyncio
from httpx import AsyncClient
from app import app
from db.db_connector import db

@pytest_asyncio.fixture(scope="function")
async def setup_db():
    await db.connect()
    yield
    await db.close()

@pytest_asyncio.fixture
async def async_client(setup_db):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
