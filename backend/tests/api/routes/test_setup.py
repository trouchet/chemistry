import toml


from backend.app import settings


def test_pong(client):
    route = f"{settings.API_V1_STR}/ping"
    response = client.get(route)

    assert response.status_code == 200
    assert response.json() == {"message": "pong"}


def test_health_check(client):
    with open("pyproject.toml", "r") as f:
        config = toml.load(f)
        version = config["tool"]["poetry"]["version"]

    route = f"{settings.API_V1_STR}/health"

    response = client.get(route)
    assert response.status_code == 200
    assert response.json() == {
        "message": "Visit /docs for more information.",
        "name": "fastapi-API",
        "status": "OK",
        "version": version,
    }


def test_info(client):
    route = f"{settings.API_V1_STR}/info"
    response = client.get(route)
    assert response.status_code == 200
    assert "name" in response.json()
    assert "version" in response.json()
    assert "description" in response.json()
