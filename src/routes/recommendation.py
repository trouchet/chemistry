from os import getcwd
from fastapi import APIRouter, Body
from ast import literal_eval

from src.logging import logging
from src.utils.dataframe import read_data_from_file
from src.core.recommendation.models import SVRecommender
from src.models import Basket, Recommendation

router = APIRouter()

is_demo = True

def demo_client_data():
    '''
    This function is a demo data loader.
    '''

    # Data file path
    filename = 'orders_sample.csv'

    sets_column = 'order_id'
    items_column = 'item_id'
    description_column = 'description'
    datapath = getcwd() + '/data/' + filename
    
    df = read_data_from_file(datapath, sets_column, items_column)

    return sets_column, items_column, description_column, df

def SV_client_data():
    '''
    This function should be replaced by a database query or 
    any other source data loading.
    '''

    # Data file path
    sets_column = 'pedi_id'
    items_column = 'prod_id'
    description_column = 'prod_descricao'
    
    filename = 'sv_sample.xlsx'
    datapath = getcwd() + '/data/' + filename
    
    df = read_data_from_file(datapath, sets_column, items_column)

    return sets_column, items_column, description_column, df

# NOTE: Replace this function by database query or any source data loading 
def get_client_data():
    return demo_client_data() if is_demo else SV_client_data()

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