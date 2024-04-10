import pandas as pd
from random import sample
from collections import defaultdict
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

from timy import timer

from src.core.recommendation.utils import get_n_best_neighbors
from src.core.recommendation.constants import (
    AVAILABLE_METHODS,
    DEFAULT_MIN_SUPPORT,
    DEFAULT_MIN_THRESHOLD,
)
from src.utils.dataframe import listify_items
from src.utils.native import flatten_list


def get_k_best_neighbors(
    method: str,
    order: list,
    neighbors: dict,
    n_suggestions: dict,
    n_best_neighbors: int,
):
    n_best_neighbors = get_n_best_neighbors(neighbors, n_best_neighbors)

    def get_best_neighbor(item_id: str):
        return n_best_neighbors.get(item_id, {})

    best_neighbors = [list(get_best_neighbor(item_id).keys()) for item_id in order]
    all_suggestions = list(set(flatten_list(best_neighbors)))

    if method == 'arbitrary':
        suggestions = all_suggestions[:n_suggestions]

    elif method == 'random':
        suggestions = (
            all_suggestions
            if len(all_suggestions) <= n_suggestions
            else sample(all_suggestions, n_suggestions)
        )

    elif method == 'support':
        count_dict = defaultdict()

        neighbors_count_items = [
            list(get_best_neighbor(item_id).items()) for item_id in order
        ]
        neighbors_count = flatten_list(neighbors_count_items)

        for neighbor_id, count in neighbors_count:
            count_value = max(count_dict.get(neighbor_id, 0), count)
            count_dict[neighbor_id] = count_value

        suggestions = [
            best_neighbor_j
            for best_neighbor_j, _ in sorted(
                count_dict.items(), key=lambda x: x[1], reverse=True
            )
        ]

    else:
        raise ValueError(f'Available methods: {AVAILABLE_METHODS}')

    return list(set(suggestions) - set(order))


def get_frequent_items_and_rules_dict(
    df_: pd.DataFrame,
    sets_column: str,
    items_column: str,
    min_support_: float,
    min_threshold_: float,
):
    frequent_itemsets, rules = get_association_rules(
        df_, sets_column, items_column, min_support_, min_threshold_
    )

    return {'frequent_itemsets': frequent_itemsets, 'association_rules': rules}


@timer()
def get_association_rules(
    df_: pd.DataFrame,
    sets_column: str,
    items_column: str,
    min_support_=DEFAULT_MIN_SUPPORT,
    min_threshold_=DEFAULT_MIN_THRESHOLD,
):
    all_sets_list = listify_items(df_, sets_column, items_column)

    # Data transform
    te = TransactionEncoder()
    te_ary = te.fit(all_sets_list).transform(all_sets_list)

    df_encoded = pd.DataFrame(te_ary, columns=te.columns_)

    # Apriori algorithm: https://en.wikipedia.org/wiki/Apriori_algorithm
    frequent_itemsets = apriori(df_encoded, min_support=min_support_, use_colnames=True)

    # Geração de Regras de Associação
    rules = association_rules(
        frequent_itemsets, metric="confidence", min_threshold=min_threshold_
    )

    return frequent_itemsets, rules
