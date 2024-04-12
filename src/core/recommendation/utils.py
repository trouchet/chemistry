# Description: Utility functions for recommendation system.
import pandas as pd
from collections import defaultdict
from random import sample

from src.utils.dataframe import listify_items, get_unique_elements


def get_items_sample(df_: pd.DataFrame, column: str, sample_count: int):
    item_ids = get_unique_elements(df_, column)
    return list(sample(item_ids, sample_count))


def get_sets_count_per_items_dict(
    df_: pd.DataFrame, sets_column: str, items_column: str
):
    result = df_.groupby(items_column)[sets_column].count().reset_index()
    result_dict = result.set_index(items_column)[sets_column].to_dict()

    return result_dict


def get_items_neighbors_count(df_: pd.DataFrame, sets_column: str, items_column: str):
    item_ids = get_unique_elements(df_, items_column)
    sets_list = listify_items(df_, sets_column, items_column)

    item_neighbors = {item_id: defaultdict(int) for item_id in item_ids}

    for item_id in item_ids:
        set_list_with_item_id = [
            set_list for set_list in sets_list if item_id in set_list
        ]

        for set_list in set_list_with_item_id:
            set_list_without_item_id = list(set(set_list) - set([item_id]))

            for friend_id in set_list_without_item_id:
                friend_i_value = item_neighbors[item_id][friend_id]
                item_neighbors[item_id][friend_id] = friend_i_value + 1

    return {key: value for key, value in item_neighbors.items() if len(value) != 0}


def get_sets_count_per_items(df_: pd.DataFrame, sets_column: str, items_column: str):
    # Group by items_column and count sets_column, then reset the index
    counts = df_.groupby(items_column)[sets_column].count().reset_index()

    # Rename the count column
    counts = counts.rename(columns={sets_column: 'count'})

    # Sort the DataFrame by the count column in descending order
    counts = counts.sort_values(by='count', ascending=False)

    return counts


def get_sets_to_items_dict(df_: pd.DataFrame, sets_column: str, items_column: str):
    # Group by 'sets_column' and aggregate 'items_column' into a list
    result = df_.groupby(sets_column)[items_column].agg(list).reset_index()

    # Convert to list of lists
    items_per_sets = result[[items_column]].values.tolist()
    sets_id = list(result[sets_column])

    return {
        set_id: list(set_items[0]) for set_id, set_items in zip(sets_id, items_per_sets)
    }
