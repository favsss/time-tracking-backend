from re import M
from fastapi.testclient import TestClient
from fastapi import status
from app.main import app
from app.sql import crud, schemas

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

def test_update_tag(db, tags):
    client = TestClient(app)
    tag = crud.get_tag_by_name(db, "project-x")

    updated_tag_name = "project-xyz"
    response = client.patch(f"/tags/{tag.id}",json={
        "name" : updated_tag_name
    })

    assert status.HTTP_200_OK == response.status_code
    data = response.json()
    assert updated_tag_name == data["name"]

def test_update_tag_duplicate(db, tags):
    client = TestClient(app)
    tag = crud.get_tag_by_name(db, "project-x")
    updated_tag_name = "Project-y"

    response = client.patch(f"/tags/{tag.id}", json={
        "name" : updated_tag_name
    })

    assert status.HTTP_400_BAD_REQUEST == response.status_code

def test_delete(db, tags):
    client = TestClient(app)
    tag = crud.get_tag_by_name(db, "project-x")

    response = client.delete(f"/tags/{tag.id}")
    
    assert status.HTTP_200_OK == response.status_code

    response = client.get("/tags")
    data = response.json()
    assert 1 == len(data)

def test_delete_nonexistent_tag(db, tags):
    client = TestClient(app)
    invalid_id = -1 

    response = client.delete(f"/tags/{invalid_id}")

    assert status.HTTP_404_NOT_FOUND == response.status_code

def test_get_users(db, users):
    client = TestClient(app)

    response = client.get("/users")

    assert status.HTTP_200_OK == response.status_code
    assert 2 == len(response.json())

def test_get_user(db, users):
    username = "applemab"
    user = crud.get_user_by_username(db, username)

    client = TestClient(app)

    response = client.get(f"/users/{user.id}")

    assert status.HTTP_200_OK == response.status_code
    assert username == response.json()["username"] 

def test_get_user_does_not_exist(db, users):
    invalid_id = -1

    client = TestClient(app)

    response = client.get(f"/users/{invalid_id}")

    assert status.HTTP_404_NOT_FOUND == response.status_code

def test_create_user(db, users):
    username = "andybon"
    password = "pacio1345"
    user_type = "Regular"

    client = TestClient(app)

    response = client.post("/users/", json={
        "username": username,
        "password": password
    })

    assert status.HTTP_200_OK == response.status_code

    data = response.json()

    assert username == data["username"]
    assert user_type == data["type"]

def test_create_user_duplicate(db, users):
    username = "applemab"
    password = "pacio1134"
    
    client = TestClient(app)

    response = client.post("/users/", json={
        "username" : username,
        "password" : password
    })

    assert status.HTTP_400_BAD_REQUEST == response.status_code

def test_delete_user(db, users):
    user = crud.get_user_by_username(db, "applemab")

    client = TestClient(app)

    response = client.delete(f"/users/{user.id}")

    assert status.HTTP_200_OK == response.status_code

    response = client.get("/users")
    assert 1 == len(response.json())

def test_delete_user_does_not_exist(db, users):
    invalid_id = -1

    client = TestClient(app)

    response = client.delete(f"/users/{invalid_id}")

    assert status.HTTP_404_NOT_FOUND == response.status_code


def test_token(db, users):
    credentials = {
        "username" : "applemab",
        "password" : "biniapple1234"
    }

    client = TestClient(app)

    response = client.post("/token", data={
        "username" : credentials["username"],
        "password" : credentials["password"]
    })

    print(response.json())

def test_get_checkins(db, checkins):
    credentials = {
        "username" : "applemab",
        "password" : "biniapple1234"
    }

    client = TestClient(app)

    response = client.post("/token", data={
        "username" : credentials["username"],
        "password" : credentials["password"]
    })

    data = response.json()
    token = data["access_token"]

    response = client.get("/checkins", headers={
        "Authorization" : f"Bearer {token}"
    })

    assert status.HTTP_200_OK == response.status_code
    assert 1 == len(response.json())

def test_get_checkin(db, checkins):
    user = crud.get_user_by_username(db, "applemab")

    credentials = {
        "username" : "applemab",
        "password" : "biniapple1234"
    }

    client = TestClient(app)

    response = client.post("/token", data={
        "username" : credentials["username"],
        "password" : credentials["password"]
    })

    token = response.json()["access_token"]

    db_checkin = crud.create_checkin(db, user.id, schemas.CheckinCreate(hours=4.5, activity="debugging", tag="project-x"))

    response = client.get(f"/checkins/{db_checkin.id}", headers={
        "Authorization" : f"Bearer {token}"
    })

    assert status.HTTP_200_OK == response.status_code

    data = response.json()

    assert 4.5 == data["hours"] 
    assert "debugging" == data["activity"]

def test_get_checkin_checkin_does_not_exist(db, checkins):
    credentials = {
        "username" : "applemab",
        "password" : "biniapple1234"
    }

    client = TestClient(app)

    response = client.post("/token", data={
        "username" : credentials["username"],
        "password" : credentials["password"]
    })

    token = response.json()["access_token"]
    invalid_id = -1

    response = client.get(f"/checkins/{invalid_id}", headers={
        "Authorization" : f"Bearer {token}"
    })

    assert status.HTTP_400_BAD_REQUEST == response.status_code

def test_get_checkin_unauthorized_user(db, checkins):
    user = crud.get_user_by_username(db, "joerizaw")

    credentials = {
        "username" : "applemab",
        "password" : "biniapple1234"
    }

    client = TestClient(app)

    response = client.post("/token", data={
        "username" : credentials["username"],
        "password" : credentials["password"]
    })

    token = response.json()["access_token"]
    db_checkin = crud.create_checkin(db, user.id, schemas.CheckinCreate(hours=4.5, activity="debugging", tag="project-x"))

    response = client.get(f"/checkins/{db_checkin.id}", headers={
        "Authorization" : f"Bearer {token}"
    })

    assert status.HTTP_401_UNAUTHORIZED == response.status_code