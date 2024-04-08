from collections import defaultdict
import pandas as pd
from random import sample 

from src.utils.dataframe import listify_items, get_unique_elements

def get_items_sample(
    df_: pd.DataFrame,
    column: str,
    sample_count: int
):
    '''
    Get a sample of items from a DataFrame column.
    '''

    item_ids = get_unique_elements(df_, column)
    return list(sample(item_ids, sample_count))

def get_sets_count_per_items_dict(
    df_: pd.DataFrame,
    sets_column: str,
    items_column: str
):
    '''
    Get the count of sets per item.
    '''
    
    result = df_.groupby(items_column)[sets_column].count().reset_index()
    result_dict = result.set_index(items_column)[sets_column].to_dict()

    return result_dict

def get_items_neighbors_count(
    df_:pd.DataFrame,
    sets_column: str,
    items_column: str
):
    '''
    Get the count of neighbors per item.
    '''

    item_ids = get_unique_elements(df_, items_column)
    sets_list = listify_items(df_, sets_column, items_column)

    item_neighbors = {
        item_id: defaultdict(int) for item_id in item_ids
    }
    
    for item_id in item_ids:
        set_list_with_item_id = [
            set_list for set_list in sets_list if item_id in set_list
        ]

        for set_list in set_list_with_item_id:
                set_list_without_item_id = list(set(set_list)-set([item_id]))
    
                for friend_id in set_list_without_item_id:
                    friend_i_value = item_neighbors[item_id][friend_id]
                    item_neighbors[item_id][friend_id] = friend_i_value + 1
            

    return {
        item_id: dict(neighbors)
        for item_id, neighbors in item_neighbors.items()
        if len(neighbors) != 0
    }