from fastapi.testclient import TestClient
from fastapi import status
from app.main import app
from app.sql import crud

def test_get_tags(tags):
    client = TestClient(app)

    response = client.get("/tags")

    assert status.HTTP_200_OK == response.status_code

    data = response.json()

    assert len(data) == 2

def test_get_tag(db, tags):
    tag = crud.get_tag_by_name(db, "project-x")
    client = TestClient(app)

    response = client.get(f"/tags/{tag.id}")

    assert status.HTTP_200_OK == response.status_code
    data = response.json()
    assert "project-x" == data["name"]

def test_get_tag_does_not_exist(db, tags):
    client = TestClient(app)

    response = client.get(f"/tags/{-1}")

    assert status.HTTP_404_NOT_FOUND  == response.status_code

def test_create_tag_lowercases_input(db, tags):
    client = TestClient(app)
    response = client.post("/tags/", json={
        "name" : "Project-z"
    })

    assert status.HTTP_200_OK == response.status_code 
    data = response.json()
    assert "project-z" == data["name"]

def test_create_tag_already_exist(db, tags):
    client = TestClient(app)
    response = client.post("/tags/", json={
        "name" : "Project-x"
    })

    assert status.HTTP_400_BAD_REQUEST == response.status_code 