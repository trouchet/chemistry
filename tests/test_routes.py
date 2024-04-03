from src.routes.recommendation import get_client_data

'''
# TO FIX: Add authentication to the API
def test_token_endpoint(client):
    # Simulate a request with a user object
    response = client.post("/api/token", json={"username": "test_user"})
    assert response.status_code == 200
    assert "access_token" in response.json()
'''

def test_recommend_product_valid(client, mock_get_client_data):
    basket_request = {"items": ["apple", "banana"]}
    response = client.post("/api/recommendation/basket", json=basket_request)
    
    assert response.status_code == 200
    assert "items" in response.json()
    assert isinstance(response.json()["items"], list)

def test_recommend_product_valid(client, mock_get_client_data):
    basket_request = {"items": ["apple", "banana"]}
    response = client.post("/api/recommendation/basket", json=basket_request)
    assert response.status_code == 200
    assert "items" in response.json()
    assert isinstance(response.json()["items"], list)

def test_recommend_product_empty_basket(client, mock_get_client_data):
    basket_request = {"items": []}
    response = client.post("/api/recommendation/basket", json=basket_request)
    assert response.status_code == 200
    assert "items" in response.json()
    assert response.json()["items"] == []

def test_get_client_data(mocker):
    # Mocking read_data_from_file
    file_alias = 'src.routes.recommendation.read_data_from_file'
    mocker.patch(file_alias, return_value='mocked_df')

    sets_column, items_column, description_column, df_ = get_client_data()

    assert sets_column == 'order_id'
    assert items_column == 'item_id'
    assert description_column == 'description'
    assert df_ == 'mocked_df'

def test_recommend_product_missing_items(client, mock_get_client_data):
    # Inexistent pear item
    basket_request = {"items": ["apple", "banana", "grape", "pear"]}
    response = client.post("/api/recommendation/basket", json=basket_request)

    assert response.status_code == 200
    assert "items" in response.json()
    
    # Only items present in the dataframe should be recommended
    items = list(response.json()["items"])
    assert len(items) <= 3

def test_recommend_product_invalid_request(client, mock_get_client_data):
    response = client.post("/api/recommendation/basket", json={})
    assert response.status_code == 200

    # Test case with invalid basket items
    response = client.post("/api/recommendation/basket", json={"items": "invalid_data"})
    assert response.status_code == 422
