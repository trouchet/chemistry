from fastapi import APIRouter
from typing import Union

from src.core.recommendation.models import (
    Product,
    Basket,
    Recommendation,
    SVRecommender,
    product_to_basket
)
from src.utils.routes import get_client_data

router = APIRouter()

@router.post(
    "/affiliate", 
    tags=["recommendation"], 
    response_model=Recommendation, 
    summary="Recommend products based on a basket."
)
async def recommend_basket(
    basket_product: Union[Product, Basket]
) -> Recommendation:
    is_product = isinstance(basket_product, Product)
    if(is_product):
        items_basket = product_to_basket(basket_product)
    else:
        items_basket = basket_product
    
    sets_col, items_col, description_col, df = get_client_data(items_basket)

    recommender = SVRecommender(df, sets_col, items_col, description_col)

    items = items_basket.model_dump().get('items', [])

    is_empty_basket = len(items) == 0
    recommendation_items = (
        [] if is_empty_basket else recommender.recommend(items)
    )

    return Recommendation(items=recommendation_items)
