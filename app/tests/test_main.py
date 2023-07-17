# This is a WIP !!
from fastapi.testclient import TestClient
from ..main import app

client = TestClient(app)

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

def test_create_valid_category():
    response = client.post("/categories", json=create_category_json)
    assert response.status_code == 201, response.text
    # data = response.json()
    # assert "id" in data

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