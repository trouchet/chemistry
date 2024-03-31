from fastapi.testclient import TestClient
import pandas as pd
from unittest.mock import patch
import pytest
import os

from src.app_factory import create_app
from src.core.recommendation.models import SVRecommender


@pytest.fixture
def sample_dict():
    return {
        'a': [1, 2, 3],
        'b': [2, 4, 6],
        'c': [3, 6, 9]
    }

@pytest.fixture
def mangled_sample_dict():
    return {
        'a': [1, 2, 3],
        'b': [2, 4, 6],
        'c': 5  # Value is not a list
    }

@pytest.fixture
def sample_list():
    return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

@pytest.fixture
def sample_df():
    return pd.DataFrame({
        'sets_column': [1, 1, 2, 2, 3, 3],
        'items_column': ['a', 'b', 'c', 'd', 'e', 'f'],
        'description_column': ['desc_a', 'desc_b', 'desc_c', 'desc_d', 'desc_e', 'desc_f'],
        'date_column': [
            '2022-01-01', 
            '2022-01-02', 
            '2023-01-01', 
            '2023-01-02', 
            '2024-01-01', 
            '2024-01-02'
        ]
    })

@pytest.fixture
def mock_read_data_to_dataframe_gen():
    with patch('src.utils.dataframe.read_data_to_dataframe_gen') as mock_gen:
        yield mock_gen

@pytest.fixture
def test_app():
    return create_app()

@pytest.fixture
def client(test_app):
    return TestClient(test_app)

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

@pytest.fixture
def sv_recommender():
    df = pd.read_csv('tests/sample_orders.csv')
    recommender = SVRecommender(
        df,
        sets_column='order_id',
        items_column='item_id',
        description_column='description'
    )
    recommender._update_neighbors()
    return recommender 

@pytest.fixture
def sample_dataframe():
    data = {
        'order_id': [1, 1, 2, 2, 3],
        'item_id': ['A', 'B', 'A', 'B', 'C']
    }
    return pd.DataFrame(data)

@pytest.fixture
def simple_dataframe():
    data = {
        'column_name': ['A', 'B', 'C', 'D', 'E']
    }
    return pd.DataFrame(data)