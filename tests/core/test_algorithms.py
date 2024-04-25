from api.core.recommendation.algorithms import (
    get_k_best_metrics,
    get_frequent_items_and_rules_dict,
)
from api.core.recommendation.utils import get_items_neighbors_count
from api.core.recommendation.metrics import get_association_metrics


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


def test_get_k_best_metrics(simple_dataframe):
    items_neighbors_count = get_items_neighbors_count(
        simple_dataframe, 
        "order_id", 
        "item_id"
    )
    metrics = get_association_metrics(
        simple_dataframe, 
        items_neighbors_count, 
        'order_id', 
        'item_id'
    )

    k_best_metrics = get_k_best_metrics(metrics, 3)

    assert k_best_metrics == {'A': {'B': 2 / 3}, 'B': {'A': 2 / 3}, 'C': {}}

    k_best_metrics = get_k_best_metrics(metrics, 3, 'confidence')

    assert k_best_metrics == {'A': {'B': 1}, 'B': {'A': 1}, 'C': {}}

    k_best_metrics = get_k_best_metrics(metrics, 3, 'lift')

    assert k_best_metrics == {'A': {'B': 1.5}, 'B': {'A': 1.5}, 'C': {}}
