from os import getcwd
from fastapi import APIRouter

from src.logging import logging
from src.utils.dataframe import read_data_from_file
from src.core.recommendation.models import SVRecommender
from src.models import Basket


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


@router.post("/basket")
async def recommend_product(
    request: Basket
):
    sets_col, items_col, description_col, df  = get_client_data()
    
    recommender = SVRecommender(df, sets_col, items_col, description_col)
    recommender._update_neighbors()

    try:
        basket = list(basket.items)
    except Exception as e:
        logging.error(e)

        return {"error": "Invalid basket items. It must be a serialized list!"}
    
    recommendation = recommender.recommend(basket)

    logging.debug(recommendation)

    return str(recommendation)