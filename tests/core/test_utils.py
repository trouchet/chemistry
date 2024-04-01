import pandas as pd
from src.core.recommendation.constants import N_BEST_NEIGHBORS_DEFAULT
from src.core.recommendation.utils import (
    get_items_sample,
    get_sets_count_per_items_dict,
    get_items_neighbors_count,
    get_n_best_neighbors,
    get_sets_count_per_items,
    get_sets_to_items_dict
)
from collections import defaultdict

def test_get_items_sample(sample_dataframe):
    sample_count = 2
    items_sample = get_items_sample(sample_dataframe, 'item_id', sample_count)
    assert len(items_sample) == sample_count

def test_get_sets_count_per_items_dict(simple_dataframe):
    sets_count_dict = get_sets_count_per_items_dict(simple_dataframe, 'order_id', 'item_id')
    assert sets_count_dict == {'A': 2, 'B': 2, 'C': 1}

def test_get_items_neighbors_count(simple_dataframe):
    neighbors_count = get_items_neighbors_count(simple_dataframe, 'order_id', 'item_id')
    expected = defaultdict(lambda: defaultdict(int))
    expected['A']['B'] = 2
    expected['B']['A'] = 2

    assert neighbors_count == expected

def test_get_n_best_neighbors():
    neighbors = {
        'A': {'B': 1, 'C': 2},
        'B': {'A': 3, 'C': 1},
        'C': {'A': 2, 'B': 2}
    }
    n_best_neighbors = get_n_best_neighbors(neighbors, 1)
    assert n_best_neighbors == {'A': {'C': 2}, 'B': {'A': 3}, 'C': {'A': 2}}

def test_get_sets_count_per_items(simple_dataframe):
    counts = get_sets_count_per_items(simple_dataframe, 'order_id', 'item_id')
    df = pd.DataFrame({'item_id': ['A', 'B', 'C'], 'count': [2, 2, 1]})
    
    assert counts.equals(df)

def test_get_sets_to_items_dict(simple_dataframe):
    sets_to_items_dict = get_sets_to_items_dict(simple_dataframe, 'order_id', 'item_id')
    
    assert sets_to_items_dict == {1: ['A', 'B'], 2: ['A', 'B'], 3: ['C']}
