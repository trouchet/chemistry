from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_token_endpoint():
    # Simulate a request with a user object
    response = client.post("/api/token", json={"username": "test_user"})
    assert response.status_code == 200
    assert "access_token" in response.json()