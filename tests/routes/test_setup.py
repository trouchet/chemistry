def test_pong(client):
    response = client.get("/api/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "pong"}


def test_health_check(client):
    import toml
    
    with toml.open("pyproject.toml") as f:
        version = f["tool"]["poetry"]["version"]

    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {
        'message': 'Visit /docs for more information.',
        'name': 'fastapi-API',
        'status': 'OK',
        'version': version,
    }


def test_info(client):
    response = client.get("/api/info")
    assert response.status_code == 200
    assert "name" in response.json()
    assert "version" in response.json()
    assert "description" in response.json()
