from src.core.recommendation.constants import N_BEST_NEIGHBORS_DEFAULT

'''
# TO FIX: Add authentication to the API
def test_token_endpoint(client):
    # Simulate a request with a user object
    response = client.post("/api/token", json={"username": "test_user"})
    assert response.status_code == 200
    assert "access_token" in response.json()
'''

BASKET_ROUTE = "/api/recommendation/basket"


def test_recommend_product_valid(client, sample_basket_factory):
    basket_request = sample_basket_factory(["apple", "banana"]).model_dump()
    response = client.post(BASKET_ROUTE, json=basket_request)

    assert response.status_code == 200
    assert "items" in response.json()
    assert isinstance(response.json()["items"], list)


def test_recommend_product_empty_basket(client, sample_basket_factory):
    basket_request = sample_basket_factory([]).model_dump()

    response = client.post(BASKET_ROUTE, json=basket_request)

    assert response.status_code == 200
    assert "items" in response.json()
    assert response.json()["items"] == []


def test_recommend_product_missing_items(client, sample_basket_factory):
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


def test_recommend_product_invalid_request(
    client,
):
    response = client.post(BASKET_ROUTE, json={})
    assert response.status_code == 200

    # Test case with invalid basket items
    invalid_basket = {"company_id": "acme", "items": "invalid_data"}
    response = client.post(BASKET_ROUTE, json=invalid_basket)
    assert response.status_code == 422
