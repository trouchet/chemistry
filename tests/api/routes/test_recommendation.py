from src.api.core.recommendation.constants import N_BEST_NEIGHBORS_DEFAULT
from fastapi.testclient import TestClient


BASKET_ROUTE = "/api/recommendation/affiliates"


def test_recommend_product_valid(client: TestClient, sample_basket_factory: callable):
    basket_request = sample_basket_factory(["apple", "banana"]).model_dump()
    response = client.post(BASKET_ROUTE, json=basket_request)

    assert response.status_code == 200
    assert "items" in response.json()
    assert isinstance(response.json()["items"], list)


def test_recommend_product_empty_basket(
    client: TestClient, sample_basket_factory: callable
):
    basket_request = sample_basket_factory([]).model_dump()

    response = client.post(BASKET_ROUTE, json=basket_request)

    assert response.status_code == 200
    assert "items" in response.json()
    assert response.json()["items"] == []


def test_recommend_product_missing_items(
    client: TestClient, sample_basket_factory: callable
):
    # Inexistent pear item
    basket_request = sample_basket_factory(
        ["apple", "banana", "grape", "pear"]
    ).model_dump()

    response = client.post(BASKET_ROUTE, json=basket_request)

    assert response.status_code == 200
    assert "items" in response.json()

    # Only items present in the dataframe should be recommended
    items = list(response.json()["items"])
    assert len(items) <= N_BEST_NEIGHBORS_DEFAULT


def test_recommend_product_(client: TestClient, sample_product_factory: callable):
    product_request = sample_product_factory("apple").model_dump()

    response = client.post(BASKET_ROUTE, json=product_request)

    assert response.status_code == 200
    assert "items" in response.json()
    assert isinstance(response.json()["items"], list)


def test_recommend_product_invalid_request(client: TestClient):
    # Test case with invalid basket items
    invalid_basket = {"company_id": "acme", "items": "invalid_data"}
    response = client.post(BASKET_ROUTE, json=invalid_basket)
    assert response.status_code == 422

