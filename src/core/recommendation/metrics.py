# Description: Functions to calculate association metrics between
# items in a dataset.

import pandas as pd

from src.core.recommendation.extract_transform import get_sets_count_per_items_dict
from src.utils.dataframe import get_unique_elements


def get_items_support(sets_count_dict: dict, sets_total: int):
    '''
    P(A) = n_A/n
    '''
    return {item_id: count / sets_total for item_id, count in sets_count_dict.items()}


def get_items_neighbors_support(item_to_neighbors_dict: dict, sets_total: int):
    '''
    P(A and B) = n_A_and_B/n
    '''
    return {
        item_id: {
            neighbor_id: neighbor_count / sets_total
            for neighbor_id, neighbor_count in neighbors.items()
        }
        for item_id, neighbors in item_to_neighbors_dict.items()
    }


def get_items_confidence(
    item_to_neighbors_dict: dict, items_support_dict: dict, sets_total: int
):
    '''
    P(B_given_A) = P(A and B) / P(A)
    '''

    neighbors_support_dict = get_items_neighbors_support(
        item_to_neighbors_dict, sets_total
    )

    return {
        item_id: {
            neighbor_id: neighbor_support / items_support_dict[item_id]
            for neighbor_id, neighbor_support in neighbors.items()
        }
        for item_id, neighbors in neighbors_support_dict.items()
    }


def get_items_lift(items_supports_dict: dict, confidences_dict: dict):
    '''
    Lift: P(B_given_A) / P(B)
    '''
    return {
        item_id: {
            neighbor_id: neighbor_confidence / items_supports_dict[neighbor_id]
            for neighbor_id, neighbor_confidence in this_item_confidences.items()
        }
        for item_id, this_item_confidences in confidences_dict.items()
    }


def get_neighbor_association_metrics(
    item_id: str,
    neighbor_id: str,
    items_support_dict: dict,
    neighbors_confidence_dict: dict,
    neighbors_lift_dict: dict,
):
    item_support = items_support_dict[item_id]
    neighbor_support = items_support_dict[neighbor_id]
    neighbor_confidence = neighbors_confidence_dict[item_id][neighbor_id]
    neighbor_lift = neighbors_lift_dict[item_id][neighbor_id]

    return {
        'support': neighbor_support,
        'confidence': neighbor_confidence,
        'lift': neighbor_lift,
        'leverage': neighbor_support - item_support * item_support,
        'conviction': (
            float('inf')
            if neighbor_confidence == 1
            else (1 - item_support) / (1 - neighbor_confidence)
        ),
    }


def get_items_association_metrics(
    item_id: str,
    neighbors_dict: dict,
    items_support_dict: dict,
    neighbors_confidence_dict: dict,
    neighbors_lift_dict: dict,
):
    '''
    Função: get_items_association_metrics

    Descrição:
    Calcula as métricas de associação para um item e seus vizinhos com base em dicionários de suporte,
    confiança e elevação.

    Parâmetros:
    - item_id (str): O ID do item para o qual as métricas serão calculadas.
    - neighbors_dict (dict): Um dicionário contendo os vizinhos de cada item.
    - items_support_dict (dict): Um dicionário contendo o suporte de cada item.
    - neighbors_confidence_dict (dict): Um dicionário contendo a confiança dos vizinhos de cada item.
    - neighbors_lift_dict (dict): Um dicionário contendo a elevação dos vizinhos de cada item.

    Retorno:
    - dict: Um dicionário contendo as métricas de associação para o item e seus vizinhos. As métricas
    incluem o suporte do item e um dicionário de vizinhos com suas métricas de associação.
    '''
    return {
        'support': items_support_dict[item_id],
        'neighbors': (
            dict()
            if neighbors_dict.get(item_id) is None
            else {
                neighbor_id: get_neighbor_association_metrics(
                    item_id,
                    neighbor_id,
                    items_support_dict,
                    neighbors_confidence_dict,
                    neighbors_lift_dict,
                )
                for neighbor_id in neighbors_dict[item_id]
            }
        ),
    }


def get_association_metrics(
    df_: pd.DataFrame, neighbors_dict: dict, sets_column: str, items_column: str
):
    '''
    Função: get_association_metrics

    Descrição:
    Calcula as métricas de associação (suporte, confiança, elevação, alavancagem e convicção)
    para todos os itens em um DataFrame com base em dicionários de vizinhos, contagem de conjuntos
    por item e suporte dos itens.

    Parâmetros:
    - df_ (pd.DataFrame): O DataFrame contendo os dados.
    - neighbors_dict (dict): Um dicionário contendo os vizinhos de cada item.
    - sets_column (str): O nome da coluna no DataFrame que contém os conjuntos de itens.
    - items_column (str): O nome da coluna no DataFrame que contém os IDs dos itens.

    Retorno:
    - dict: Um dicionário contendo as métricas de associação para cada item. Cada item tem um dicionário
    com suas métricas de associação, incluindo suporte, confiança, elevação, alavancagem e convicção.
    '''
    sets_count_dict = get_sets_count_per_items_dict(df_, sets_column, items_column)

    sets_total = len(get_unique_elements(df_, sets_column))

    items_support_dict = get_items_support(sets_count_dict, sets_total)
    neighbors_confidence_dict = get_items_confidence(
        neighbors_dict, items_support_dict, sets_total
    )
    neighbors_lift_dict = get_items_lift(items_support_dict, neighbors_confidence_dict)

    # Association metrics:
    #
    # Support: P(A and B)
    # Confidence: P(B_given_A) = P(A and B) / P(A)
    # Lift: P(B_given_A) / P(B)
    # Leverage: P(A and B) - P(A) * P(B)
    # Conviction: (1 - P(B)) / (1 - P(B_given_A))

    return {
        item_id: get_items_association_metrics(
            item_id,
            neighbors_dict,
            items_support_dict,
            neighbors_confidence_dict,
            neighbors_lift_dict,
        )
        for item_id in items_support_dict
    }
