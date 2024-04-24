from fastapi.testclient import TestClient
import pandas as pd
from unittest.mock import patch
import pytest
import os
from os import getcwd, path

from src.app import app
from src.core.recommendation.models import \
    SVRecommender, \
    Product, \
    Item, \
    Basket

from src.core.recommendation.metrics import (
    get_neighbor_association_metrics,
)

## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
## Samples
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
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
def simple_dataframe():
    data = {'order_id': [1, 1, 2, 2, 3], 'item_id': ['A', 'B', 'A', 'B', 'C']}
    return pd.DataFrame(data)


@pytest.fixture
def simplest_dataframe():
    data = {'column_name': ['A', 'B', 'C', 'D', 'E']}
    return pd.DataFrame(data)


@pytest.fixture
def recommendation_dataframe():
    filename = "fruits_sample.csv"
    folder = 'tests/data'
    filepath = path.join(getcwd(), folder, filename)
    
    return pd.read_csv(filepath)


## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
## src/routes
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
@pytest.fixture
def company_id():
    return 'acme'


@pytest.fixture
def sample_basket_factory(company_id):
    def factory(items: list) -> Basket:
        return Basket(company_id=company_id, items=items, is_demo=True)

    return factory


@pytest.fixture
def sample_product_factory(company_id):
    def factory(item: str) -> Basket:
        return Product(
            company_id=company_id, 
            product_id=item, 
            is_demo=True)

    return factory


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def mock_get_client_data(mocker, sample_dataframe):
    return mocker.patch(
        'src.routes.recommendation.get_client_data',
        return_value=('order_id', 'item_id', 'description', sample_dataframe),
    )


## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
## src/utils/native
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
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
    path = 'src.utils.dataframe.read_data_to_dataframe_gen'

    with patch(path) as mock_gen:
        yield mock_gen


## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
## src/utils
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
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


## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
## src/core/recommendation/models
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
@pytest.fixture
def sample_item():
    return Item(identifier='apple', value=0.5)

@pytest.fixture
def sv_recommender(recommendation_dataframe):
    recommender = SVRecommender(
        recommendation_dataframe,
        sets_column='order_id',
        items_column='item_id',
        description_column='description',
    )
    return recommender

@pytest.fixture
def small_sample_items():
    return ["apple", "banana"]

@pytest.fixture
def small_sample_description():
    return ['Description of apple', 'Description of banana']

@pytest.fixture
def sample_sets_info():
    df_dict = {
        'sets': [1, 1, 1, 2, 2, 3],
        'items': ['A', 'B', 'C', 'A', 'B', 'A'],
    }

    df = pd.DataFrame(df_dict)
    set_count = { 'A': 3, 'B': 2, 'C': 1,}
    neighbors = { 
        'A': { 'B': 2, 'C': 1, },
        'B': { 'A': 2, 'C': 1, },
        'C': { 'A': 1, 'B': 1, },
    }
    expected = {
        "item_support": { 'A': 1, 'B': 2 / 3, 'C': 1 / 3, },
        "neighbors_support": {
            'A': { 'B': 2 / 3, 'C': 1 / 3, },
            'B': { 'A': 2 / 3, 'C': 1 / 3, },
            'C': { 'A': 1 / 3, 'B': 1 / 3, },
        },
        "neighbors_confidence": {
            'A': { 'B': 2 / 3, 'C': 1 / 3, },
            'B': { 'A': 1, 'C': 1 / 2, },
            'C': { 'A': 1, 'B': 1, },
        },
        "neighbors_lift": {
            'A': {'B': 1, 'C': 1},
            'B': {'A': 1, 'C': 3 / 2},
            'C': {'A': 1, 'B': 3 / 2},
        },
    }

    expected_dataframe_metrics = {
        item_id: {
            'support': expected["item_support"][item_id],
            'neighbors': {
                neighbor_id: get_neighbor_association_metrics(
                    item_id, neighbor_id,
                    expected['item_support'],
                    expected['neighbors_confidence'],
                    expected['neighbors_lift'],
                ) for neighbor_id in neighbors
            },
        }
        for item_id, neighbors in neighbors.items()
    }

    return {
        "dataframe": df,
        "total": 3,
        "set_column": "sets",
        "item_column": "items",
        "sets_count": set_count,
        "neighbors": neighbors,
        "expected": expected,
        "expected_metrics": expected_dataframe_metrics
    }

@pytest.fixture
def sv_recommender_small_base(recommendation_dataframe):
    recommender = SVRecommender(
        recommendation_dataframe,
        sets_column='order_id',
        items_column='item_id',
        description_column='description',
    )
    return recommender

## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
## src/core/recommendation/algorithms
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
@pytest.fixture
def neighbors_data():
    return {
        'item1': { 'neighbor1': 1, 'neighbor2': 2 },
        'item2': { 'neighbor3': 3, 'neighbor4': 4 },
    }


@pytest.fixture
def order_data():
    return ['item1', 'item2']
