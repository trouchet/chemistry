from fastapi.testclient import TestClient
import pandas as pd
from unittest.mock import patch
import pytest
import os

from src.app_factory import create_app
from src.core.recommendation.models import \
    SVRecommender, \
    Basket, \
    Product

## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
## Samples
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
@pytest.fixture
def sample_dataframe():
    return pd.DataFrame(
        {
            'order_id': [1, 1, 2, 2, 3, 3],
            'item_id': ['a', 'b', 'c', 'd', 'e', 'f'],
            'description': ['desc_a', 'desc_b', 'desc_c', 'desc_d', 'desc_e', 'desc_f'],
            'purchase_date': [
                '2022-01-01',
                '2022-01-02',
                '2023-01-01',
                '2023-01-02',
                '2024-01-01',
                '2024-01-02',
            ],
        }
    )


@pytest.fixture
def fruits_dataframe():
    # Create a sample DataFrame for testing
    data = {
        'order_id': [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 5, 5],
        'item_id': [
            'apple',
            'banana',
            'orange',
            'banana',
            'orange',
            'grape',
            'apple',
            'banana',
            'grape',
            'apple',
            'grape',
            'banana',
            'orange',
        ],
        'description': [
            'Description of apple',
            'Description of banana',
            'Description of orange',
            'Description of banana',
            'Description of orange',
            'Description of grape',
            'Description of apple',
            'Description of banana',
            'Description of grape',
            'Description of apple',
            'Description of grape',
            'Description of banana',
            'Description of orange',
        ],
    }

    return pd.DataFrame(data)


@pytest.fixture
def simple_dataframe():
    data = {'order_id': [1, 1, 2, 2, 3], 'item_id': ['A', 'B', 'A', 'B', 'C']}
    return pd.DataFrame(data)


@pytest.fixture
def simplest_dataframe():
    data = {'column_name': ['A', 'B', 'C', 'D', 'E']}
    return pd.DataFrame(data)


@pytest.fixture
def recommendation_dataframe():
    return pd.read_csv('tests/sample_orders.csv')


## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
## src/routes
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
@pytest.fixture
def test_app():
    return create_app()


@pytest.fixture
def company_id():
    return 'acme'


@pytest.fixture
def sample_basket_factory(company_id):
    def factory(items: list) -> Basket:
        return Basket(company_id=company_id, items=items, is_demo=True)

    return factory


@pytest.fixture
def sample_item_factory(company_id):
    def factory(item: str) -> Basket:
        return Product(company_id=company_id, id=item, is_demo=True)

    return factory


@pytest.fixture
def client(test_app):
    return TestClient(test_app)


@pytest.fixture
def mock_get_client_data(mocker, sample_dataframe):
    return mocker.patch(
        'src.routes.recommendation.get_client_data',
        return_value=('order_id', 'item_id', 'description', sample_dataframe),
    )


## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
## src/utils/native
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
@pytest.fixture
def sample_dict():
    return {'a': [1, 2, 3], 'b': [2, 4, 6], 'c': [3, 6, 9]}


@pytest.fixture
def mangled_sample_dict():
    return {'a': [1, 2, 3], 'b': [2, 4, 6], 'c': {'foo': 'bar'}}  # Value is not a list


@pytest.fixture
def sample_list():
    return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


@pytest.fixture
def mock_read_data_to_dataframe_gen():
    with patch('src.utils.dataframe.read_data_to_dataframe_gen') as mock_gen:
        yield mock_gen


## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
## src/utils
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
@pytest.fixture
def sample_data():
    return {'a': 1, 'b': [2, 3, 4], 'c': {'d': 5, 'e': 6}}


@pytest.fixture
def pkl_filepath(tmp_path):
    return os.path.join(tmp_path, 'test.pkl')


@pytest.fixture
def dill_filepath(tmp_path):
    return os.path.join(tmp_path, 'test.dill')


@pytest.fixture
def cloudpickle_filepath(tmp_path):
    return os.path.join(tmp_path, 'test_cloudpickle.pkl')


## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
## src/core/recommendation/models
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
@pytest.fixture
def sv_recommender(recommendation_dataframe):
    recommender = SVRecommender(
        recommendation_dataframe,
        sets_column='order_id',
        items_column='item_id',
        description_column='description',
    )
    return recommender


## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
## src/core/recommendation/algorithms
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
@pytest.fixture
def neighbors_data():
    return {
        'item1': {'neighbor1': 1, 'neighbor2': 2},
        'item2': {'neighbor3': 3, 'neighbor4': 4},
    }


@pytest.fixture
def order_data():
    return ['item1', 'item2']
