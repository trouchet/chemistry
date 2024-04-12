# Description: Recommendation models for the recommender system.
import pandas as pd
import logging
from reprlib import repr

from pydantic import model_validator, BaseModel, Field
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

        if demo_type is not None and \
            demo_type not in ['small', 'medium', 'big', 'huge']:
            raise ValueError("demo_type must be one of: small, medium, big, huge")

        if is_demo and not demo_type:
            values['demo_type'] = 'small'

        return values


# Request model
class Product(RecommendationResource):
    product_id: str

# Request model
class Basket(RecommendationResource):
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


def product_to_basket(product: Product) -> Basket:
    return Basket(
        company_id=product.company_id, 
        items=[product.product_id], 
        algorithm=product.algorithm,
        neighbors_count=product.neighbors_count,
        age_months=product.age_months,
        is_demo=product.is_demo,
        demo_type=product.demo_type
    )

# Object Item
class Item:
    def __init__(self, identifier: str, value: float, description: str = None):
        self.identifier = identifier
        self.value = value
        self.description = description or f"Description of {identifier}"

    def __repr__(self):
        return f"Item(identifier={self.identifier}, value={self.value})"
    

# Response model
class Recommendation(BaseModel):
    items: Optional[List[str]] = []
    metadata: Optional[dict] = {}


class SVRecommender(object):
    """
    This class is responsible for providing recommendations based on
    the provided DataFrame. It uses an heuristic approach to suggest
    items that are frequently bought together.

    Parameters
    ----------

    df_: pd.DataFrame
        DataFrame containing the data to be used for recommendation
    sets_column: str
        Column name containing the sets
    items_column: str
        Column name containing the items
    description_column: str
        Column name containing the description of the items
    n_suggestions: int
        Number of suggestions to be provided
    n_best_neighbors: int
        Number of best neighbors to be considered
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
        self.neighbors_dict = get_items_neighbors_count(
            self.data_dataframe, self.__sets_column, self.__items_column
        )

    def association_metrics(self):
        """
        Get association metrics
        """
        self._update_neighbors()
        
        return get_association_metrics(
            self.data_dataframe,
            self.neighbors_dict,
            self.__sets_column,
            self.__items_column,
        )

    def recommend(self, order: list, method: str = RECOMMENDATION_ALGO_DEFAULT):
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
        described_items = []

        for item_id in item_ids:
            try:
                described_items.append(self.descriptions_dict[item_id])
            except Exception:
                described_items.append('')

        return described_items
