from src.core.recommendation.itemset_generator import ItemSetsGenerator
from src.utils.dataframe import get_unique_elements


def test_itemset_generator():
    num_itemsets = 10
    num_items = 100
    num_agents = 10
    quantity_interval = (10, 20)
    value_interval = (0.01, 1000)
    mean_items_per_itemset = 10

    itemset_generator = ItemSetsGenerator(
        num_itemsets,
        num_items,
        num_agents,
        quantity_interval,
        value_interval,
        mean_items_per_itemset,
    )

    df = itemset_generator.generate()

    itemsets_len = len(get_unique_elements(df, 'itemset_id'))
    assert itemsets_len == num_itemsets

    itemsets_agent_ids = get_unique_elements(df, 'agent_id')
    expected_agent_ids = set(itemset_generator.agent_ids)
    this_agent_ids = set(itemsets_agent_ids)
    intersection_ids = this_agent_ids.intersection(expected_agent_ids)

    assert len(intersection_ids) > 0
