import pytest

from src.core.recommendation.algorithms import (
    get_k_best_neighbors,
    get_frequent_items_and_rules_dict,
)
from src.core.recommendation.constants import AVAILABLE_METHODS


def test_get_frequent_items_and_rules_dict(recommendation_dataframe):
    # Test the function with the sample DataFrame
    min_support = 0.2
    min_threshold = 0.5
    sets_column = 'order_id'
    items_column = 'item_id'
    result = get_frequent_items_and_rules_dict(
        recommendation_dataframe, 
        sets_column, items_column, 
        min_support, min_threshold
    )

    assert isinstance(result, dict)
    assert 'frequent_itemsets' in result
    assert 'association_rules' in result
    assert not result['frequent_itemsets'].empty
    assert not result['association_rules'].empty


def test_get_k_best_neighbors_invalid_method():
    with pytest.raises(ValueError) as exc_info:
        order = ['item1', 'item2', 'item3']
        neighbors = {'item1': {'item2': 1, 'item3': 2}, 'item2': {'item1': 3}}
        method = 'invalid_method'
        n_suggestions = 2
        n_best_neighbors = 2
        get_k_best_neighbors(method, order, neighbors, n_suggestions, n_best_neighbors)

    assert str(exc_info.value) == f"Available methods: {AVAILABLE_METHODS}"
