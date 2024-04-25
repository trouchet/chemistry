from reprlib import repr

from pydantic import BaseModel, Field, model_validator
from typing import Optional, List

from api.core.recommendation.constants import   (
        RECOMMENDATION_ALGO_DEFAULT, \
        N_BEST_NEIGHBORS_DEFAULT
    )

from api.constants import VALID_AGE_MONTHS, DEFAULT_AGE

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
        demo_type=product.demo_type
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

class Item(BaseModel):
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