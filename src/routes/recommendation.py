from os import getcwd
from fastapi import APIRouter

from src.models import RecommendationResponse, BasketRequest
from src.core.recommendation.models import SVRecommender
from src.utils.dataframe import read_data_from_file

router = APIRouter()

def get_client_data():
    sets_column = 'pedi_id'
    items_column = 'prod_id'
    description_column = 'prod_descricao'
    datapath = getcwd() + '/data'
    
    df_ = read_data_from_file(datapath, sets_column, items_column)
    
    return sets_column, items_column, description_column, df_ 

@router.post(
    "/basket", response_model=RecommendationResponse, status_code=200
)
async def recommend_product(request: BasketRequest):
    sets_col, items_col, description_col, df  = get_client_data()
    
    recommender = SVRecommender(df, sets_col, items_col, description_col)
    recommender._update_neighbors()
    
    recommendation = recommender.recommend(request.basket)

    return {"recommendation": str(recommendation)}