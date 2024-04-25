# Description: Recommendation models for the recommender system.
import pandas as pd
import logging
from reprlib import repr

from pydantic import BaseModel, Field, model_validator
from typing import Optional, List

from src.core.recommendation.algorithms import get_k_best_neighbors
from .extract_transform import get_sets_count_per_items_dict, get_items_neighbors_count
from src.utils.dataframe import listify_items, get_descriptions
from src.core.recommendation.metrics import get_association_metrics

from src.core.recommendation.constants import (
    N_BEST_NEIGHBORS_DEFAULT,
    RECOMMENDATION_ALGO_DEFAULT,
    N_SUGGESTIONS_DEFAULT,
    AVAILABLE_METHODS,
)

from src.constants import VALID_AGE_MONTHS, DEFAULT_AGE


class RecommendationResource(BaseModel):
    company_id: str = Field(default='demo')
    algorithm: Optional[str] = RECOMMENDATION_ALGO_DEFAULT
    neighbors_count: Optional[int] = N_BEST_NEIGHBORS_DEFAULT
    age_months: Optional[int] = DEFAULT_AGE
    is_demo: Optional[bool] = False
    demo_type: str = Field('small', description='One of: small, medium, big, huge')

    @model_validator(mode="before")
    @classmethod
    def validate_demo_type(cls, values):
        is_demo = values.get('is_demo')
        demo_type = values.get('demo_type')

        if demo_type is not None and demo_type not in [
            'small',
            'medium',
            'big',
            'huge',
        ]:
            raise ValueError("demo_type must be one of: small, medium, big, huge")

        if is_demo and not demo_type:
            values['demo_type'] = 'small'

        return values


#################### Modelos de requisição ####################


# Produto
class Product(RecommendationResource):
    """
    Classe para representar um produto.

    Attributes:
        product_id (str): O ID do produto.
        Os demais atributos são herdados da classe RecommendationResource.
    """

    product_id: str


# Carrinho
class Basket(RecommendationResource):
    """
    Classe para representar um carrinho de compras.

    Attributes:
        items (List[str]): Uma lista de IDs de produtos no carrinho.
        Os demais atributos são herdados da classe RecommendationResource.

    Methods:
        is_age_valid(): Verifica se age_months está dentro de VALID_AGE_MONTHS.
    """

    items: List[str] = Field(default=[])

    def is_age_valid(self):
        """
        Checks if age_months is within VALID_AGE_MONTHS
        """
        return self.age_months in VALID_AGE_MONTHS

    def __eq__(self, other):
        """
        Compares two baskets for equality based on their items.
        """
        if not isinstance(other, Basket):
            return False

        return (
            self.items == other.items
            and self.company_id == other.company_id
            and self.algorithm == other.algorithm
            and self.neighbors_count == other.neighbors_count
            and self.age_months == other.age_months
        )

    def __ne__(self, other):
        """
        Compares two baskets for inequality based on their items.
        """
        return not self.__eq__(other)

    def __repr__(self) -> None:
        return f"Basket(company_id={self.company_id}, items={repr(self.items)})"


# Converte 'Product' para 'Basket'
def product_to_basket(product: Product) -> Basket:
    return Basket(
        company_id=product.company_id,
        items=[product.product_id],
        algorithm=product.algorithm,
        neighbors_count=product.neighbors_count,
        age_months=product.age_months,
        is_demo=product.is_demo,
        demo_type=product.demo_type,
    )


# Recomendação
class Recommendation(BaseModel):
    """
    Classe para representar uma recomendação de itens.

    Attributes:
        items (Optional[List[str]]): Uma lista opcional de IDs de itens recomendados.
        metadata (Optional[dict]): Metadados opcionais adicionais.

    """

    items: Optional[List[str]] = []
    metadata: Optional[dict] = {}


# Object Item
class Item:
    """
    Classe para representar um item.

    Attributes:
        identifier (str): O identificador do item.
        value (float): O valor do item.
        description (str): A descrição do item (padrão: 'Description of {identifier}').

    """

    def __init__(self, identifier: str, value: float, description: str = None):
        self.identifier = identifier
        self.value = value
        self.description = description or f"Description of {identifier}"

    def __repr__(self):
        return f"Item(identifier={self.identifier}, value={self.value})"


class SVRecommender(object):
    """
    Classe para recomendação de itens com base em conjuntos de itens anteriores.

    Args:
        df_ (pd.DataFrame): O DataFrame contendo os dados.
        sets_column (str): O nome da coluna contendo os conjuntos.
        items_column (str): O nome da coluna contendo os item_ids.
        description_column (str): O nome da coluna contendo as descrições dos itens.
        n_suggestions (int): O número de sugestões a serem feitas (padrão: N_SUGGESTIONS_DEFAULT).
        n_best_neighbors (int): O número de melhores vizinhos a serem considerados (padrão: N_BEST_NEIGHBORS_DEFAULT).

    Attributes:
        data_dataframe (pd.DataFrame): O DataFrame contendo os dados.
        descriptions_dict (dict): Um dicionário contendo as descrições dos itens.
        order_list (list): Uma lista de conjuntos de itens em cada pedido.
        orders_per_product_dict (dict): Um dicionário com a contagem de conjuntos únicos em que cada item aparece.
        neighbors_dict (dict): Um dicionário representando os vizinhos de cada item e a contagem de vezes que eles aparecem nos mesmos conjuntos.
        n_suggestions (int): O número de sugestões a serem feitas.
        n_best_neighbors (int): O número de melhores vizinhos a serem considerados.

    Methods:
        association_metrics(): Retorna as métricas de associação.
        recommend(order: list, method: str = RECOMMENDATION_ALGO_DEFAULT): Retorna uma lista de recomendações com base no pedido fornecido.
        describe(item_ids: list): Retorna as descrições dos itens fornecidos.
    """

    def __init__(
        self,
        df_: pd.DataFrame,
        sets_column: str,
        items_column: str,
        description_column: str,
        n_suggestions: int = N_SUGGESTIONS_DEFAULT,
        n_best_neighbors: int = N_BEST_NEIGHBORS_DEFAULT,
    ):

        if n_suggestions <= 0 or n_best_neighbors <= 0:
            error_message = 'Number of provided suggestions or best neighbors must be greater than 0!'
            raise ValueError(error_message)

        self.data_dataframe = df_

        self.__sets_column = sets_column
        self.__items_column = items_column

        self.descriptions_dict = get_descriptions(df_, items_column, description_column)
        self.order_list = listify_items(df_, sets_column, items_column)
        self.orders_per_product_dict = get_sets_count_per_items_dict(
            df_, sets_column, items_column
        )
        self.neighbors_dict = {}
        self.n_suggestions = n_suggestions
        self.n_best_neighbors = n_best_neighbors

    def _update_neighbors(self):
        """
        Atualiza o dicionário de vizinhos dos itens.
        """
        self.neighbors_dict = get_items_neighbors_count(
            self.data_dataframe, self.__sets_column, self.__items_column
        )

    def association_metrics(self):
        """
        Retorna as métricas de associação.
        """
        self._update_neighbors()

        return get_association_metrics(
            self.data_dataframe,
            self.neighbors_dict,
            self.__sets_column,
            self.__items_column,
        )

    def recommend(self, order: list, method: str = RECOMMENDATION_ALGO_DEFAULT):
        """
        Retorna uma lista de recomendações com base no pedido fornecido.

        Args:
            order (list): A lista de itens do pedido.
            method (str): O método de recomendação a ser utilizado (padrão: RECOMMENDATION_ALGO_DEFAULT).

        Returns:
            list: Uma lista de itens recomendados.
        """
        logging.info(f'Running recommendation with method: {method}')
        metrics = self.association_metrics()

        # Empty dataframe or without neighbors
        if len(self.neighbors_dict) == 0:
            return []

        # Get the best neighbors
        if method in AVAILABLE_METHODS:
            return get_k_best_neighbors(
                method,
                order,
                metrics,
                self.n_suggestions,
                self.n_best_neighbors,
            )

        else:
            raise ValueError(f'Available methods: {AVAILABLE_METHODS}')

    def describe(self, item_ids: list):
        """
        Retorna as descrições dos itens fornecidos.

        Args:
            item_ids (list): A lista de item_ids.

        Returns:
            list: Uma lista de descrições dos itens.
        """

        described_items = []

        for item_id in item_ids:
            try:
                described_items.append(self.descriptions_dict[item_id])
            except Exception:
                described_items.append('')

        return described_items
