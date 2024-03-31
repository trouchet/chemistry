from fastapi.testclient import TestClient
import pandas as pd
from unittest.mock import patch
import pytest

from src.app_factory import create_app

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
    return create_app(0)

@pytest.fixture
def client(test_app):
    return TestClient(test_app)