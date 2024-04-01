from unittest.mock import patch
import pytest

from src.core.recommendation.extract_transform import get_items_sample

def test_get_items_sample(simplest_dataframe):
    column_name = 'column_name'
    sample_count = 2

    result = get_items_sample(simplest_dataframe, column_name, sample_count)

    assert len(result) == sample_count
