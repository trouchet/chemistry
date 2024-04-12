from src.core.recommendation.metrics import (
    get_items_support,
    get_items_neighbors_support,
    get_items_confidence,
    get_items_lift,
    get_association_metrics,
    get_neighbor_association_metrics,
)


def test_get_items_support(sample_sets_info):
    sets_count_dict = sample_sets_info["sets_count"]
    sets_total = sample_sets_info["total"]
    expected_items_support = sample_sets_info["expected"]["item_support"]

    items_support = get_items_support(sets_count_dict, sets_total)

    assert items_support == expected_items_support


def test_get_items_neighbors_support(sample_sets_info):
    sets_neighbors_dict = sample_sets_info["neighbors"]
    sets_total = sample_sets_info["total"]
    expected_neighbors_support = sample_sets_info["expected"]["neighbors_support"]

    neighbors_support = get_items_neighbors_support(sets_neighbors_dict, sets_total)

    assert neighbors_support == expected_neighbors_support


def test_get_items_confidence(sample_sets_info):
    sets_count_dict = sample_sets_info["sets_count"]
    sets_neighbors_dict = sample_sets_info["neighbors"]
    sets_total = sample_sets_info["total"]
    expected_neighbors_confidence = sample_sets_info["expected"]["neighbors_confidence"]

    items_support_dict = get_items_support(sets_count_dict, sets_total)

    neighbors_confidence = get_items_confidence(
        sets_neighbors_dict, items_support_dict, sets_total
    )

    assert expected_neighbors_confidence == neighbors_confidence


def test_get_items_lift(sample_sets_info):
    sets_count_dict = sample_sets_info["sets_count"]
    sets_neighbors_dict = sample_sets_info["neighbors"]
    expected_neighbors_lift_dict = sample_sets_info["expected"]["neighbors_lift"]
    sets_total = sample_sets_info["total"]

    items_support_dict = get_items_support(sets_count_dict, sets_total)
    items_confidence_dict = get_items_confidence(
        sets_neighbors_dict, items_support_dict, sets_total
    )

    neighbors_lift_dict = get_items_lift(items_support_dict, items_confidence_dict)

    assert neighbors_lift_dict == expected_neighbors_lift_dict


def test_get_items_support_empty():
    sets_count_dict = {}
    sets_total = 0

    items_support = get_items_support(sets_count_dict, sets_total)

    assert items_support == {}


def test_association_metrics(sample_sets_info):
    df = sample_sets_info["dataframe"]
    set_column = sample_sets_info["set_column"]
    item_column = sample_sets_info["item_column"]
    sets_neighbors_dict = sample_sets_info["neighbors"]
    expected_metrics = sample_sets_info["expected_metrics"]
    
    dataframe_metrics = get_association_metrics(
        df, sets_neighbors_dict, set_column, item_column
    )

    assert dataframe_metrics == expected_metrics
