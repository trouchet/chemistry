import json

from src.utils.routes import make_json_response


def test_make_json_response():
    response = make_json_response(200, {"key": "value"})

    assert response.status_code == 200
    assert json.loads(response.body.decode()) == {"key": "value"}
