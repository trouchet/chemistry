from os import getcwd
from fastapi import APIRouter, Body
from src.logging import logging

from src.core.recommendation.models import SVRecommender
from src.utils.dataframe import read_data_from_file

router = APIRouter()

# TAKE NOTE: 
#   Replace this function by database query or any source data loading 
def get_client_data():
    # Data file path
    filename = 'orders_sample.csv'

    sets_column = 'pedi_id'
    items_column = 'prod_id'
    description_column = 'prod_descricao'
    datapath = getcwd() + '/data/' + filename
    
    df = read_data_from_file(datapath, sets_column, items_column)
    
    return sets_column, items_column, description_column, df

from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str
    price: float
    tax: float

@router.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()

    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    
    return item_dict

from typing import List

# Request model
class BasketRequest(BaseModel):
    basket: str

# Response model
class RecommendationResponse(BaseModel):
    recommendation: str

@router.post("/basket")
async def recommend_product(
    request: BasketRequest = Body(...)
):
    sets_col, items_col, description_col, df  = get_client_data()
    
    recommender = SVRecommender(df, sets_col, items_col, description_col)
    recommender._update_neighbors()

    basket = list(request.basket)
    recommendation = recommender.recommend(basket)

    logging.debug(recommendation)

    return str(recommendation)