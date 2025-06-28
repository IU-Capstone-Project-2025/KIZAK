import pytest
from faker import Faker
from ..db.db_connector import db
from fastapi.testclient import TestClient
from ..models.resource import ResourceCreate, ResourceResponse, ResourceUpdate


def test_post_resource():
    faker = Faker()
    user = {
    }


def test_get_resource():
    ...


def test_update_resource():
    ...


def test_get_post_put_delete_resource():
    ...
