# Description: This file contains functions to extract and transform
# data for recommendation systems.
from collections import defaultdict
import pandas as pd
from random import sample

from src.api.utils.dataframe import listify_items, get_unique_elements


def get_items_sample(df_: pd.DataFrame, column: str, sample_count: int):
    '''
    Função: get_items_sample

    Descrição:
    Esta função recebe um DataFrame, o nome de uma coluna e um número de amostras e 
    retorna uma lista com uma amostra aleatória de itens únicos da coluna especificada.

    Parâmetros:
    - df_ (pd.DataFrame): O DataFrame contendo os dados.
    - column (str): O nome da coluna da qual se deseja obter a amostra.
    - sample_count (int): O número de amostras a serem obtidas.

    Retorno:
    - list: Uma lista com a amostra aleatória de itens únicos da coluna especificada.
    '''

    item_ids = get_unique_elements(df_, column)
    return list(sample(item_ids, sample_count))


def get_sets_count_per_items_dict(
    df_: pd.DataFrame, sets_column: str, items_column: str
):
    '''
    Função: get_sets_count_per_items_dict

    Descrição:
    Esta função recebe um DataFrame, o nome de uma coluna de conjuntos, e o nome de uma 
    coluna de itens, e retorna um dicionário onde as chaves são os itens e os valores são 
    o número de conjuntos em que cada item aparece.

    Parâmetros:
    - df_ (pd.DataFrame): O DataFrame contendo os dados.
    - sets_column (str): O nome da coluna que contém os conjuntos.
    - items_column (str): O nome da coluna que contém os itens.

    Retorno:
    - dict: Um dicionário onde as chaves são os itens e os valores são o número de conjuntos 
    em que cada item aparece.
    '''

    result = df_.groupby(items_column)[sets_column].count().reset_index()
    result_dict = result.set_index(items_column)[sets_column].to_dict()

    return result_dict


def get_items_neighbors_count(df_: pd.DataFrame, sets_column: str, items_column: str):
    '''
    Função: get_items_neighbors_count

    Descrição:
    Esta função recebe um DataFrame, o nome de uma coluna de conjuntos, e o nome de uma coluna 
    de itens, e retorna um dicionário onde as chaves são os itens e os valores são outros 
    dicionários contendo o número de vizinhos de cada item.

    Parâmetros:
    - df_ (pd.DataFrame): O DataFrame contendo os dados.
    - sets_column (str): O nome da coluna que contém os conjuntos.
    - items_column (str): O nome da coluna que contém os itens.

    Retorno:
    - dict: Um dicionário onde as chaves são os itens e os valores são dicionários contendo o 
    número de vizinhos de cada item.
    '''
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

    return {
        item_id: dict(neighbors)
        for item_id, neighbors in item_neighbors.items()
        if len(neighbors) != 0
    }
