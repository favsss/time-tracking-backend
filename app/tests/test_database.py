from fastapi.testclient import TestClient

from app.main import app

def test_smoke_test(db):
    client = TestClient(app)

    response = client.get("/")

    assert response.status_code == 200