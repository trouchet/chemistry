from secrets import choice
from string import ascii_letters, digits
from scipy.stats import poisson
from typing import Union
from random import sample
import pandas as pd

# Default size of token
DEFAULT_TOKEN_LENGTH = 10


def generate_random_tokens(
    num_tokens: int = 1, token_length: int = DEFAULT_TOKEN_LENGTH
):
    """
    Generate random tokens.

    Args:
        num_tokens (int, optional): Number of tokens to generate. Defaults to 1.
        token_length (int, optional): Length of each token. Defaults to DEFAULT_TOKEN_LENGTH.

    Returns:
        list: List of generated tokens.

    Examples:
        >>> len(generate_random_tokens())
        1
        >>> len(generate_random_tokens(5))
        5
        >>> all(len(token) == DEFAULT_TOKEN_LENGTH for token in generate_random_tokens())
        True
        >>> all(len(token) == 10 for token in generate_random_tokens(5, 10))
        True
    """

    tokens = []
    for _ in range(num_tokens):
        token = ''.join(choice(ascii_letters + digits) for _ in range(token_length))
        tokens.append(token)

    return tokens


def generate_item_ids(num_items: int):
    return generate_random_tokens(num_items, DEFAULT_TOKEN_LENGTH)


def generate_item_dict(itemset_id: Union[int, str], item_ids: list):
    # Randomly select an item id for items
    item_id = sample(item_ids, 1)[0]

    item_description = f"Description of item {item_id}"
    item_dict = {
        'order_id': itemset_id,
        'item_id': item_id,
        'description': item_description,
    }

    return item_dict


def generate_itemset_list(itemset_id: int, item_ids: list):
    # Mean number of items per itemsets
    mean_items_per_itemset = 5

    # Generate bin sizes using Poisson distribution
    itemset_size = poisson.rvs(mean_items_per_itemset, size=1)[0]

    itemsets = []
    for item in range(itemset_size):
        item_dict = generate_item_dict(itemset_id, item_ids)
        itemsets.append(item_dict)

    return itemsets


def generate_itemsets_dataframe(num_items: int, num_itemsets):
    # Generate available item ids
    item_ids = generate_item_ids(num_items)

    # Generate orders, items, and descriptions
    itemsets = []
    for itemset_id in range(num_itemsets):
        itemset_id_ = itemset_id + 1

        itemset = generate_itemset_list(itemset_id_, item_ids)
        itemsets = itemsets + itemset

    # Create a DataFrame from the generated data
    return pd.DataFrame(itemsets)
