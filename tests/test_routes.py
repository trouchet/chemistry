from src.core.recommendation.constants import N_BEST_NEIGHBORS_DEFAULT
from fastapi.testclient import TestClient

'''
# TO FIX: Add authentication to the API
def test_token_endpoint(client):
    # Simulate a request with a user object
    response = client.post("/api/token", json={"username": "test_user"})
    assert response.status_code == 200
    assert "access_token" in response.json()
'''

BASKET_ROUTE = "/api/recommendation/affiliates"
def test_recommend_product_valid(
    client: TestClient, 
    sample_basket_factory: callable
):
    basket_request = sample_basket_factory(["apple", "banana"]).model_dump()
    response = client.post(BASKET_ROUTE, json=basket_request)

    assert response.status_code == 200
    assert "items" in response.json()
    assert isinstance(response.json()["items"], list)


def test_recommend_product_empty_basket(
    client: TestClient, 
    sample_basket_factory: callable
):
    basket_request = sample_basket_factory([]).model_dump()

    response = client.post(BASKET_ROUTE, json=basket_request)

    assert response.status_code == 200
    assert "items" in response.json()
    assert response.json()["items"] == []


def test_recommend_product_missing_items(
    client: TestClient, 
    sample_basket_factory: callable
):
    # Inexistent pear item
    basket_request = sample_basket_factory(
        ["apple", "banana", "grape", "pear"]
    ).model_dump()
    print(basket_request)
    response = client.post(BASKET_ROUTE, json=basket_request)

    assert response.status_code == 200
    assert "items" in response.json()

    # Only items present in the dataframe should be recommended
    items = list(response.json()["items"])
    assert len(items) <= N_BEST_NEIGHBORS_DEFAULT


def test_recommend_product_(
    client: TestClient, 
    sample_product_factory: callable 
):
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

"""
def test_create_user(client: TestClient):
    # Define a user object to send in the request
    user_data = {
        "username": "testuser",
        "password": "testpassword"
    }

    # Send a POST request to the /users endpoint
    response = client.post("/api/users", json=user_data)

    # Assert the response status code and content
    assert response.status_code == 201
    assert response.json() == {"message": "User created successfully"}

    # Test case where user already exists
    response = client.post("/users", json=user_data)
    assert response.status_code == 400
    assert response.json() == {"error": "User already exists"}

    # Test case where an exception is raised
    response = client.post("/users", json={"username": "testuser"})
    assert response.status_code == 500
    assert response.json() == {"error": "Column 'password' cannot be null"}
"""