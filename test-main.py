from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_users():
    response = client.get("/users")
    assert response.status_code == 200
    assert response.json() == []  # Assuming there are no users initially

def test_create_user():
    response = client.post("/users", json={"email": "test@example.com"})
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"
