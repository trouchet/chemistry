# Description: Utility functions for recommendation system.
import pandas as pd
from collections import defaultdict
from random import sample

from api.utils.dataframe import listify_items, get_unique_elements


def get_items_sample(df_: pd.DataFrame, column: str, sample_count: int):
    """
    Retorna uma amostra aleatória de item_ids únicos de um DataFrame.

    Args:
        df_ (pd.DataFrame): O DataFrame contendo os dados.
        column (str): O nome da coluna contendo os item_ids.
        sample_count (int): O número de item_ids a serem amostrados.

    Returns:
        List: Uma lista contendo a amostra de item_ids.
    """

    item_ids = get_unique_elements(df_, column)
    return list(sample(item_ids, sample_count))


def get_sets_count_per_items_dict(
    df_: pd.DataFrame, sets_column: str, items_column: str
):
    """
    Retorna um dicionário onde as chaves são os item_ids e os valores são o número de conjuntos
    únicos em que cada item aparece.

    Args:
        df_ (pd.DataFrame): O DataFrame contendo os dados.
        sets_column (str): O nome da coluna contendo os conjuntos.
        items_column (str): O nome da coluna contendo os item_ids.

    Returns:
        Dict: Um dicionário onde as chaves são os item_ids e os valores são o número de conjuntos
        únicos em que cada item aparece.
    """
    result = df_.groupby(items_column)[sets_column].count().reset_index()
    result_dict = result.set_index(items_column)[sets_column].to_dict()

    return result_dict


def get_items_neighbors_count(
        df_: pd.DataFrame, 
        sets_column: str, 
        items_column: str
):
    """
    Retorna um dicionário onde as chaves são os item_ids e os valores são outro dicionário
    representando os vizinhos de cada item e a contagem de vezes que eles aparecem nos mesmos conjuntos.

    Args:
        df_ (pd.DataFrame): O DataFrame contendo os dados.
        sets_column (str): O nome da coluna contendo os conjuntos.
        items_column (str): O nome da coluna contendo os item_ids.

    Returns:
        Dict: Um dicionário onde as chaves são os item_ids e os valores são outro dicionário
        representando os vizinhos de cada item e a contagem de vezes que eles aparecem nos mesmos conjuntos.
    """

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
    """
    Retorna um DataFrame contendo a contagem de conjuntos únicos em que cada item aparece,
    ordenado pela contagem em ordem decrescente.

    Args:
        df_ (pd.DataFrame): O DataFrame contendo os dados.
        sets_column (str): O nome da coluna contendo os conjuntos.
        items_column (str): O nome da coluna contendo os item_ids.

    Returns:
        pd.DataFrame: Um DataFrame contendo a contagem de conjuntos únicos em que cada item aparece,
        ordenado pela contagem em ordem decrescente.
    """

    # Group by items_column and count sets_column, then reset the index
    counts = df_.groupby(items_column)[sets_column].count().reset_index()

    # Rename the count column
    counts = counts.rename(columns={sets_column: 'count'})

    # Sort the DataFrame by the count column in descending order
    counts = counts.sort_values(by='count', ascending=False)

    return counts


def get_sets_to_items_dict(df_: pd.DataFrame, sets_column: str, items_column: str):
    '''
    Retorna um dicionário onde as chaves são os conjuntos únicos no DataFrame e os 
    valores são as listas de itens associadas a cada conjunto.

    Parâmetros:
    - df_: DataFrame: O DataFrame contendo os dados.
    - sets_column: str: O nome da coluna que contém os conjuntos.
    - items_column: str: O nome da coluna que contém os itens.

    Retorna:
    - dict: Um dicionário onde as chaves são os conjuntos e os valores são listas de 
    itens associadas a cada conjunto.
    '''

    # Group by 'sets_column' and aggregate 'items_column' into a list
    result = df_.groupby(sets_column)[items_column].agg(list).reset_index()

    # Convert to list of lists
    items_per_sets = result[[items_column]].values.tolist()
    sets_id = list(result[sets_column])

    return {
        set_id: list(set_items[0]) for set_id, set_items in zip(sets_id, items_per_sets)
    }
