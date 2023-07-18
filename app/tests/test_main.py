# This is a WIP !!
import pytest
import asyncio
import pytest_asyncio

from fastapi.testclient import TestClient
from app.main import app
from app.lib.sql import *

client = TestClient(app)

## https://stackoverflow.com/questions/74351637/pytest-with-async-tests-test-setup-before-and-after
@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

## Droping all tables and rebuild database to have clean data
@pytest_asyncio.fixture(scope="session", autouse=True)
async def fixture_clear_database():
    await drop_tables()
    await build_database()


## Default json for each entity
create_category_json = {
    "name": "My Category"
}

create_member_json = {
    "username": "John123",
    "firstname": "John",
    "lastname": "Doe",
    "description": "Who am I ?",
    "mail": "john@doe.com",
    "url_portfolio": "www.doe.com"
}

## Create a valid category
def test_create_valid_category():
    response = client.post("/categories", json=create_category_json)
    assert response.status_code == 201, response.text
    # data = response.json()
    # assert "id" in data

## Create category with already used name
def test_create_category_with_same_name():
    response = client.post("/categories", json=create_category_json)
    assert response.status_code == 400

## Create category with empty name
def test_create_category_with_empty_name():
    response = client.post("/categories", json={"name":""})
    assert response.status_code == 400

# def test_create_valid_member():
#     response = client.post(
#         "/members",
#         json=create_member_json
#     )
#     assert response.status_code == 200, response.text
#     data = response.json()
#     assert id in data
#     assert date_activated in data

# def test_read_members():
#     response = client.get("/members")
#     assert response.status_code == 200
#     assert response.json() == []