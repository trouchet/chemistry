from timy import timer
import pandas as pd
import logging
from reprlib import repr
import os

from pydantic import BaseModel, Field
from typing import Optional, List

from src.core.recommendation.algorithms import get_k_best_neighbors
from .extract_transform import \
    get_sets_count_per_items_dict, \
    get_items_neighbors_count
from src.utils.dataframe import listify_items, get_descriptions
from src.core.recommendation.metrics import get_association_metrics

from src.core.recommendation.constants import (
    N_BEST_NEIGHBORS_DEFAULT,
    RECOMMENDATION_ALGO_DEFAULT,
    N_SUGGESTIONS_DEFAULT,
    AVAILABLE_METHODS,
)

from src.constants import VALID_AGE_MONTHS, DEFAULT_AGE

# Auxiliar model
class CompanyResource(BaseModel):
    company_id: str = Field(default='demo')
    is_demo: Optional[bool] = False

# Request model
class Product(CompanyResource):
    id: str

# Object Item
class Item:
    def __init__(self, identifier: str, value: float, description: str = None):
        self.identifier = identifier 
        self.value = value
        self.description = description or f"Description of {identifier}"

    def __repr__(self):
        return f"Item(identifier={self.identifier}, value={self.value})"

# Request model
class Basket(CompanyResource):
    items: List[str] = Field(default=[])
    algorithm: Optional[str] = RECOMMENDATION_ALGO_DEFAULT
    neighbors_count: Optional[int] = N_BEST_NEIGHBORS_DEFAULT
    age_months: Optional[int] = DEFAULT_AGE

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

def product_to_basket(product: Product) -> Basket:
    return Basket(
        company_id=product.company_id, 
        items=[product.id], 
        is_demo=product.is_demo
    )

# Response model
class Recommendation(BaseModel):
    items: Optional[List[str]] = []
    metadata: Optional[dict] = {}

class SVRecommender(object):
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

        self.descriptions_dict = get_descriptions(\
            df_, items_column, 
            description_column
        )
        self.order_list = listify_items(df_, sets_column, items_column)
        self.orders_per_product_dict = get_sets_count_per_items_dict(
            df_, sets_column, items_column
        )
        self.neighbors_dict = {}
        self.n_suggestions = n_suggestions
        self.n_best_neighbors = n_best_neighbors

    def _update_neighbors(self):
        neighbors = get_items_neighbors_count(
            self.data_dataframe, self.__sets_column, self.__items_column
        )

        self.neighbors_dict = neighbors

    def association_metrics(self):
        """
        Get association metrics
        """
        self._update_neighbors()
        return get_association_metrics(
            self.data_dataframe, 
            self.neighbors_dict, 
            self.__sets_column, 
            self.__items_column
        )

    @timer()
    def recommend(self, order: list, method: str = RECOMMENDATION_ALGO_DEFAULT):
        logging.info(f'Running recommendation with method: {method}')
        self._update_neighbors()

        # Empty dataframe or without neighbors
        if len(self.neighbors_dict) == 0:
            return []

        # Get the best neighbors
        if method in AVAILABLE_METHODS:
            return get_k_best_neighbors(
                method,
                order,
                self.neighbors_dict,
                self.n_suggestions,
                self.n_best_neighbors,
            )

        else:
            raise ValueError(f'Available methods: {AVAILABLE_METHODS}')

    def describe(self, item_ids: list):
        described_items = []

        for item_id in item_ids:
            try:
                described_items.append(self.descriptions_dict[item_id])
            except Exception:
                described_items.append('')

        return described_items
