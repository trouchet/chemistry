from fastapi import APIRouter, Body

from src.core.recommendation.models import (
    Product,
    Basket,
    Recommendation,
    SVRecommender,
    product_to_basket
)
from src.utils.routes import get_client_data

router = APIRouter()

@router.post("/item")
async def recommend_item(
    product: Product
) -> Recommendation:
    print(product)
    item_basket = product_to_basket(product)

    sets_col, items_col, description_col, df = get_client_data(item_basket)

    recommender = SVRecommender(df, sets_col, items_col, description_col)

    if item_basket.items:
        basket_items = item_basket.model_dump()['items']
    else:
        return Recommendation(items=[])

    recommendation_items = recommender.recommend(basket_items)

    return Recommendation(items=recommendation_items)


@router.post("/basket")
async def recommend_basket(basket: Basket) -> Recommendation:
    sets_col, items_col, description_col, df = get_client_data(basket)

    recommender = SVRecommender(df, sets_col, items_col, description_col)

    basket_items = basket.model_dump().get('items', [])

    is_empty_basket = len(basket_items) == 0
    recommendation_items = (
        [] if is_empty_basket else recommender.recommend(basket_items)
    )

    return Recommendation(items=recommendation_items)
