# Description: Module responsible for generating template itemsets
# for the recommendation system.
from scipy.stats import poisson
from typing import Union, List, Tuple
import pandas as pd
from random import uniform, randint
import uuid
from datetime import datetime, timedelta

from src.core.recommendation.models import Item
from src.core.recommendation.constants import MEAN_ITEMS_PER_ITEMSET
from src.utils.native import generate_random_tokens, get_random_element

# Types
ItemsetSizeType = Union[int, float]
StringOrUUIDList = List[Union[str, uuid.UUID]]


def get_itemset_size(mean_items_per_itemset: int):
    return poisson.rvs(mean_items_per_itemset, size=1)[0]


def generate_item_ids(num_items: int):
    return generate_random_tokens(num_items)


def generate_agent_ids(num_agents: int):
    return generate_random_tokens(num_agents)


def generate_quantity(min_qty: float, max_qty: float):
    while True:
        yield randint(min_qty, max_qty)


def generate_value(min_value: float, max_value: float):
    while True:
        value = round(uniform(min_value, max_value), 2)
        yield value


def generate_items(
    num_items: int,
    value_interval: Tuple[float],
):
    item_ids = generate_item_ids(num_items)

    # Generate available item ids
    def item_factory(item_props: Tuple):
        identifier = item_props[0]
        value = item_props[1]

        return Item(identifier, value)

    min_value, max_value = value_interval

    value_gen = generate_value(min_value, max_value)
    item_props_zip = zip(item_ids, value_gen)
    items = list(map(item_factory, item_props_zip))

    return items


def generate_item_dict(
    itemset_id: Union[int, str], agent_id: str, item: Item, quantity: int
):
    return {
        'itemset_id': itemset_id,
        'agent_id': agent_id,
        'item_id': item.identifier,
        'item_description': item.description,
        'item_quantity': quantity,
        'item_value': item.value,
    }

def generate_set_timestamp(start_year: int, end_year: int):
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year, 12, 31)
    days_between = (end_date - start_date).days
    random_days = randint(0, days_between)
    return start_date + timedelta(days=random_days)

def generate_quantified_item(items: List[Item], quantity_interval: Tuple[float]):
    item = get_random_element(items)

    min_qty = quantity_interval[0]
    max_qty = quantity_interval[1]
    quantity = next(generate_quantity(min_qty, max_qty))

    return item, quantity


class ItemSetsGenerator:
    def __init__(
        self,
        time_interval: Tuple[int],
        num_itemsets: int,
        num_items: int,
        num_agents: int,
        quantity_interval: Tuple[int],
        value_interval: Tuple[float],
        mean_items_per_itemset: int = MEAN_ITEMS_PER_ITEMSET,
    ):
        self.time_interval = time_interval
        self.num_itemsets = num_itemsets
        self.num_items = num_items
        self.num_agents = num_agents
        self.quantity_interval = quantity_interval
        self.value_interval = value_interval
        self.mean_items_per_itemset = mean_items_per_itemset

        self.items = []
        self.agent_ids = []

    def __generate_itemset_list(self, itemset_id: int, agent_id: list):
        # Generate bin sizes using Poisson distribution
        itemset_size = get_itemset_size(self.mean_items_per_itemset)
        itemset = []
        for item in range(itemset_size):
            item, quantity = generate_quantified_item(
                self.items, self.quantity_interval
            )
            item_dict = generate_item_dict(itemset_id, agent_id, item, quantity)

            itemset.append(item_dict)

        return itemset

    def generate(self):
        self.items = generate_items(self.num_items, self.value_interval)
        self.agent_ids = generate_agent_ids(self.num_agents)

        # Generate orders, items, and descriptions
        itemsets = []
        for itemset_id in range(self.num_itemsets):
            itemset_id_ = itemset_id + 1
            agent_id_ = get_random_element(self.agent_ids)
            itemset_timestamp = generate_set_timestamp(*self.time_interval)

            itemset = self.__generate_itemset_list(itemset_id_, agent_id_)
            itemsets = itemsets + itemset

        # Create a DataFrame from the generated data
        return pd.DataFrame(itemsets)
