import pandas as pd
from numpy import unique, quantile
from random import sample 
from collections import defaultdict
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

from timy import timer
from src.utils.native import flatten_list
from src.utils.dataframe import listify_items
from src.utils.file import create_folder, extend_filename
from src.utils.constants import NEIGHBORS_COUNT_DEFAULT, MIN_SET_SIZE_CONFIDENCE


def get_sets_count_per_items(
    df_: pd.DataFrame,
    sets_column: str,
    items_column: str
):
    # Group by items_column and count sets_column, then reset the index
    counts = df_.groupby(items_column)[sets_column].count().reset_index()
    
    # Rename the count column
    counts = counts.rename(columns={sets_column: 'count'})

    # Sort the DataFrame by the count column in descending order
    counts = counts.sort_values(by='count', ascending=False)
    
    return counts

def get_sets_to_items_dict(
    df_: pd.DataFrame,
    sets_column: str,
    items_column: str
):    
    # Group by 'order_id' and aggregate 'product_id' into a list
    result = listify_items(df_, sets_column, items_column)

    # Convert to list of lists
    products_per_order = result[['items_list']].values.tolist()
    orders_id = list(result[sets_column])
    
    return {
        order_id: list(unique(lst[0]))
        for order_id, lst in zip(orders_id, products_per_order) 
    }

def get_n_best_neighbors(
    neighbors: dict,
    best_neighbor_count: int = NEIGHBORS_COUNT_DEFAULT
):
    # Prune 
    max_count = max(1, best_neighbor_count)
    n_best_neighbors = {
        neighbor_id: dict(
            [
                item
                for item in sorted(
                    neighbors[neighbor_id].items(), 
                    key=lambda x: x[1], 
                    reverse=True
                )[:max_count]
            ] 
        )
        for neighbor_id in neighbors
    }

    return n_best_neighbors

def get_k_best_arbitrary_neighbors(
    order: list,
    neighbors: dict,
    n_suggestions: dict,
    n_best_neighbors: int,
):
    n_best_neighbors = get_n_best_neighbors(neighbors, n_best_neighbors)

    def get_best_neighbor(item_id: str):
        try:
            return n_best_neighbors[item_id]
        except KeyError:
            return {}

    all_suggestions = list(
        set(flatten_list([list(get_best_neighbor(item_id).keys()) for item_id in order]))
    )
    
    suggestions = all_suggestions[:n_suggestions]
    
    return list(set(suggestions) - set(order))

def get_k_best_random_neighbors(
    order: list,
    neighbors: dict,
    n_suggestions: dict,
    n_best_neighbors: int,
):
    n_best_neighbors = get_n_best_neighbors(neighbors, n_best_neighbors)

    def get_best_neighbor(item_id: str):
        try:
            return n_best_neighbors[item_id]
        except KeyError:
            return {}

    all_suggestions = list(
        set(flatten_list([list(get_best_neighbor(item_id).keys()) for item_id in order]))
    )
    
    suggestions = sample(all_suggestions, n_suggestions)
    
    return list(set(suggestions) - set(order))

def get_k_best_support_based_neighbors(
    order: list,
    neighbors_: dict,
    sets_count_dict: dict,
    n_suggestions: dict,
    n_best_neighbors: int,
):
    n_best_neighbors = get_n_best_neighbors(neighbors_, n_best_neighbors)

    def get_best_neighbor(item_id: str):
        try:
            return n_best_neighbors[item_id]
        except KeyError:
            return {}

    count_dict = defaultdict()
    for neighbor_id, count in flatten_list(
        [ list(get_best_neighbor(item_id).items()) for item_id in order ]
    ):
        try:
            count_dict[neighbor_id] = max(count_dict[neighbor_id], count)
        except KeyError:
            count_dict[neighbor_id] = count            
    
    suggestion = [
        best_neighbor_j
        for best_neighbor_j, _ in sorted(
            count_dict.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
    ][:n_suggestions]

    return list(set(suggestion) - set(order))

def get_frequent_items_and_rules_dict(
    filename_: str,
    df_: pd.DataFrame, 
    min_support_: float, 
    min_threshold_: float
):
    frequent_itemsets, rules = get_association_rules(
        df_, min_support_, min_threshold_
    )

    if(not rules.empty):
        create_folder('rules')
        new_filename = extend_filename(filename_, rules)
        rules.to_excel(new_filename)
    
    return {
        'frequent_itemsets': frequent_itemsets,
        'association_rules': rules
    }

@timer()
def get_association_rules(
    df_: pd.DataFrame, sets_column: str, items_column: str,
	min_support_=0.001,	min_threshold_=0.05, set_size_confidence=MIN_SET_SIZE_CONFIDENCE,
    is_verbose=True
):
    all_sets_list = listify_items(df_, sets_column, items_column)
    len_map = lambda x: len(x)
    len_sets = list(
        map(len_map, listify_items(df_, sets_column, items_column))
    )
    
    percentile_X = quantile(len_sets, set_size_confidence)
    confidence_data = list(filter(lambda x: len(x) < percentile_X, all_sets_list))
    
    # Data transform
    te = TransactionEncoder()
    te_ary = te.fit(confidence_data).transform(confidence_data)

    df_encoded = pd.DataFrame(te_ary, columns=te.columns_)
    
    # Apriori algorithm: https://en.wikipedia.org/wiki/Apriori_algorithm
    frequent_itemsets = apriori(df_encoded, min_support=min_support_, use_colnames=True)
    
    # Geração de Regras de Associação
    relevant_columns = ['antecedents', 'consequents', 'support', 'confidence', 'lift']
    rules = association_rules(frequent_itemsets, metric = "confidence", min_threshold = min_threshold_)

    if(is_verbose):
        print(f'Comprimento de pedidos originais : {len(all_sets_list)}')
        print(f'Comprimento de pedidos de treino : {len(confidence_data)}')
        print(f'Número de regras                 : {len(rules)}')
        print()
    
    return frequent_itemsets, rules[relevant_columns]