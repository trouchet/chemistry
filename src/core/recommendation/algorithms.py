# Description: Implementation of algorithm for generating
# itemsets and association rules.
import pandas as pd
from random import sample
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules
from timy import timer

from src.core.recommendation.constants import (
    AVAILABLE_METHODS,
    AVAILABLE_METRICS,
    DEFAULT_MIN_SUPPORT,
    DEFAULT_MIN_THRESHOLD,
    N_BEST_NEIGHBORS_DEFAULT,
)
from src.utils.dataframe import listify_items
from src.utils.native import flatten_list, setify_list


def get_k_best_metrics(
    item_to_neighbors_metrics: dict,
    best_neighbor_count: int = N_BEST_NEIGHBORS_DEFAULT,
    metric_subject: str = 'support',
):
    # Prune
    max_count = max(1, best_neighbor_count)

    return {
        item_id: dict(
            sorted(
                [
                    (neighbor_id, neighbor_metrics[metric_subject])
                    for neighbor_id, neighbor_metrics in item_to_neighbors_metrics[
                        item_id
                    ]["neighbors"].items()
                ],
                key=lambda x: x[1],
                reverse=True,
            )[:max_count]
        )
        for item_id in item_to_neighbors_metrics
    }


def get_all_suggestions(order: list, n_best_metrics: dict) -> list:
    def get_best_neighbor(item_id: str):
        return n_best_metrics.get(item_id, {})

    # Get best neighbors for each item in the order
    best_neighbors = [list(get_best_neighbor(item_id).items()) for item_id in order]

    return list(set(flatten_list(best_neighbors)))


def get_k_best_neighbors(
    method: str,
    order: list,
    item_to_neighbors_metrics: dict,
    n_suggestions: dict,
    n_best: int,
) -> list:
    if method in AVAILABLE_METRICS:
        n_best_metrics = get_k_best_metrics(item_to_neighbors_metrics, n_best, method)

        all_suggestions = flatten_list(
            [
                list(neighbors_metrics.items())
                for neighbors_metrics in n_best_metrics.values()
            ]
        )

        suggestions = setify_list(
            [
                best_neighbor_j
                for best_neighbor_j in sorted(
                    all_suggestions, key=lambda x: x[1], reverse=True
                )
            ][:n_suggestions]
        )

    elif method in ['arbitrary', 'random']:
        n_best_metrics = get_k_best_metrics(item_to_neighbors_metrics, n_best)
        all_suggestions = get_all_suggestions(order, n_best_metrics)

        if method == 'arbitrary':
            suggestions = all_suggestions[:n_suggestions]

        else:
            suggestions = (
                all_suggestions
                if len(all_suggestions) <= n_suggestions
                else sample(all_suggestions, n_suggestions)
            )

    else:
        raise ValueError(f'Available methods: {AVAILABLE_METHODS}')

    suggestions = [suggestion[0] for suggestion in suggestions]

    return list(set(suggestions) - set(order))[:n_suggestions]


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
