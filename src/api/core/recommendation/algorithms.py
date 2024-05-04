# Description: Implementation of algorithm for generating
# itemsets and association rules.
import pandas as pd
from random import sample
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules
from timy import timer

from src.api.core.recommendation.constants import (
    AVAILABLE_METHODS,
    AVAILABLE_METRICS,
    DEFAULT_MIN_SUPPORT,
    DEFAULT_MIN_THRESHOLD,
    N_BEST_NEIGHBORS_DEFAULT,
)
from src.api.utils.dataframe import listify_items
from src.api.utils.native import (
    flatten_list,
    setify_list,
    remove_duplicates_and_select_max,
)


def get_k_best_metrics(
    item_to_neighbors_metrics: dict,
    best_neighbor_count: int = N_BEST_NEIGHBORS_DEFAULT,
    metric_subject: str = 'support',
):
    '''
    Função: get_all_suggestions

    Descrição:
    Esta função recebe uma lista de IDs de itens e um dicionário contendo métricas para os melhores vizinhos de cada item. Ela retorna uma lista de IDs únicos dos melhores vizinhos de todos os itens na ordem fornecida.

    Parâmetros:
    - order (list): Uma lista de IDs de itens para os quais as sugestões serão obtidas.
    - n_best_metrics (dict): Um dicionário onde as chaves são IDs de itens e os valores são dicionários contendo métricas para os melhores vizinhos de cada item.

    Retorno:
    - list: Uma lista de IDs únicos dos melhores vizinhos de todos os itens na ordem fornecida.
    '''
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
    '''
    Função: get_all_suggestions

    Descrição:
    Esta função recebe uma lista de IDs de itens e um dicionário contendo métricas para os melhores vizinhos
    de cada item. Ela retorna uma lista de IDs únicos dos melhores vizinhos de todos os itens na ordem fornecida.

    Parâmetros:
    - order (list): Uma lista de IDs de itens para os quais as sugestões serão obtidas.
    - n_best_metrics (dict): Um dicionário onde as chaves são IDs de itens e os valores são dicionários contendo
    métricas para os melhores vizinhos de cada item.

    Retorno:
    - list: Uma lista de IDs únicos dos melhores vizinhos de todos os itens na ordem fornecida.
    '''

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
    '''
    Função: get_k_best_neighbors

    Descrição:
    Esta função recebe um método de seleção, uma ordem de itens, um dicionário contendo métricas
    para os vizinhos de cada item, o número desejado de sugestões e o número de melhores vizinhos
    a serem considerados. Com base no método de seleção fornecido, ela retorna uma lista de IDs únicos
    dos melhores vizinhos de todos os itens na ordem fornecida, excluindo os itens já presentes na ordem.

    Parâmetros:
    - method (str): O método de seleção a ser utilizado. Pode ser um dos métodos disponíveis em AVAILABLE_METRICS
    ('support', 'confidence', etc.), 'arbitrary' para selecionar os vizinhos de forma arbitrária, ou 'random' para
    selecionar vizinhos aleatórios.
    - order (list): Uma lista de IDs de itens na ordem em que devem ser considerados.
    - item_to_neighbors_metrics (dict): Um dicionário onde as chaves são IDs de itens e os valores são dicionários
    contendo métricas para os vizinhos de cada item.
    - n_suggestions (int): O número de sugestões desejadas.
    - n_best (int): O número de melhores vizinhos a serem considerados.

    Retorno:
    - list: Uma lista de IDs únicos dos melhores vizinhos de todos os itens na ordem fornecida, excluindo os itens
    já presentes na ordem, e limitada ao número de sugestões desejadas.
    '''
    if method in AVAILABLE_METRICS:
        n_best_metrics = get_k_best_metrics(item_to_neighbors_metrics, n_best, method)

        all_suggestions = flatten_list(
            [
                list(neighbors_metrics.items())
                for neighbors_metrics in n_best_metrics.values()
            ]
        )

        all_suggestions = remove_duplicates_and_select_max(all_suggestions)

        # Remove items already in the order
        all_suggestions = [
            (neighbor_id, neighbor_metric)
            for neighbor_id, neighbor_metric in all_suggestions
            if neighbor_id not in order
        ]

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

        all_suggestions = remove_duplicates_and_select_max(all_suggestions)

        # Remove items already in the order
        all_suggestions = [
            (neighbor_id, neighbor_metric)
            for neighbor_id, neighbor_metric in all_suggestions
            if neighbor_id not in order
        ]

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
    '''
    Função: get_frequent_items_and_rules_dict

    Descrição:
    Esta função recebe um DataFrame contendo transações, o nome da coluna que contém os conjuntos
    de itens em cada transação, o nome da coluna que contém os IDs dos itens, o suporte mínimo e o
    limiar mínimo para a geração de regras de associação. Ela retorna um dicionário contendo os
    itemsets frequentes e as regras de associação geradas a partir dos dados.

    Parâmetros:
    - df_ (pd.DataFrame): O DataFrame contendo as transações.
    - sets_column (str): O nome da coluna que contém os conjuntos de itens em cada transação.
    - items_column (str): O nome da coluna que contém os IDs dos itens.
    - min_support_ (float): O suporte mínimo para considerar um itemset como frequente.
    - min_threshold_ (float): O limiar mínimo para gerar regras de associação.

    Retorno:
    - dict: Um dicionário contendo dois itens: 'frequent_itemsets', que é um DataFrame dos itemsets
    frequentes, e 'association_rules', que é um DataFrame das regras de associação geradas.
    '''
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
    '''
    Função: get_association_rules

    Descrição:
    Esta função recebe um DataFrame contendo transações, o nome da coluna que contém os conjuntos
    de itens em cada transação, o nome da coluna que contém os IDs dos itens, o suporte mínimo e
    o limiar mínimo para a geração de regras de associação. Ela utiliza o algoritmo Apriori para
    encontrar os itemsets frequentes e gera regras de associação com base nos parâmetros fornecidos.

    Parâmetros:
    - df_ (pd.DataFrame): O DataFrame contendo as transações.
    - sets_column (str): O nome da coluna que contém os conjuntos de itens em cada transação.
    - items_column (str): O nome da coluna que contém os IDs dos itens.
    - min_support_ (float): O suporte mínimo para considerar um itemset como frequente. O padrão
    é DEFAULT_MIN_SUPPORT.
    - min_threshold_ (float): O limiar mínimo para gerar regras de associação. O padrão é DEFAULT_MIN_THRESHOLD.

    Retorno:
    - tuple: Uma tupla contendo dois elementos. O primeiro elemento é um DataFrame dos itemsets
    frequentes encontrados e o segundo elemento é um DataFrame das regras de associação geradas.
    '''
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
