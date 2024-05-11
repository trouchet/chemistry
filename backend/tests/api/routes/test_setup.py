import toml


from app import app


def test_pong(client):
    route = app.url_path_for("ping")
    response = client.get(route)

    # Iterate through app.router_registry potentially
    for route in app.routes:
        print(f"Path: {route}")

    assert response.status_code == 200
    assert response.json() == {"message": "pong"}


def test_health_check(client):
    with open("pyproject.toml", "r") as f:
        config = toml.load(f)
        version = config["tool"]["poetry"]["version"]

    route = app.url_path_for("health_check")
    response = client.get(route)
    assert response.status_code == 200
    assert response.json() == {
        "message": "Visit /docs for more information.",
        "name": "fastapi-API",
        "status": "OK",
        "version": version,
    }


def test_info(client):
    route = app.url_path_for("info")
    response = client.get(route)
    assert response.status_code == 200
    assert "name" in response.json()
    assert "version" in response.json()
    assert "description" in response.json()
