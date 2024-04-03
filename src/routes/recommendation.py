from os import getcwd
from fastapi import APIRouter, Body
from ast import literal_eval

from src.logging import logging
from src.utils.dataframe import read_data_from_file
from src.core.recommendation.models import SVRecommender
from src.models import Basket, Recommendation

router = APIRouter()

# NOTE: Replace this function by database query or any source data loading 
def get_client_data():
    # Data file path
    filename = 'orders_sample.csv'

    sets_column = 'order_id'
    items_column = 'item_id'
    description_column = 'description'
    datapath = getcwd() + '/data/' + filename
    
    df = read_data_from_file(datapath, sets_column, items_column)
    
    return sets_column, items_column, description_column, df

@router.post("/basket")
async def recommend_product(
    basket: Basket = Body(default={"items": []})
) -> Recommendation:
    sets_col, items_col, description_col, df  = get_client_data()
    
    recommender = SVRecommender(df, sets_col, items_col, description_col)
    recommender._update_neighbors()

    if basket.items:
        basket_items = basket.dict()['items']
    else:
        return Recommendation(items=[])

    recommendation = recommender.recommend(basket_items)

    return Recommendation(items=recommendation)