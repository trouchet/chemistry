from fastapi.testclient import TestClient
import pytest

from src.app import app

client = TestClient(app)

def test_read_root():
    response = client.get("/api/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "pong"}

def test_pong(client):
    response = client.get("/api/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "pong"}

def test_health_check(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_info(client):
    response = client.get("/api/info")
    assert response.status_code == 200
    assert "name" in response.json()
    assert "version" in response.json()
    assert "description" in response.json()
