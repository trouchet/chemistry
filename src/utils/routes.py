from os import getcwd
from fastapi.responses import JSONResponse

from src.utils.dataframe import read_data_from_file
from src.core.recommendation.models import Basket
from src.utils.dataframe import get_itemsets_with_items

def make_json_response(
    status_: int, 
    content_: dict
) -> JSONResponse:
    return JSONResponse(status_code = status_, content = content_)

def demo_client_data(basket: Basket):
    '''
    This function is a demo data loader.
    '''

    # Data file path
    filename = 'small_test_sample.csv'

    sets_column = 'order_id'
    items_column = 'item_id'
    description_column = 'description'
    datapath = getcwd() + '/data/' + filename
    
    df = read_data_from_file(datapath, sets_column, items_column)
    
    # Filter the dataframe by the basket items
    order = basket.model_dump()["items"]

    df = get_itemsets_with_items(df, order, sets_column, items_column)

    return sets_column, items_column, description_column, df

# NOTE: Replace this function by database query or any source data loading 
def SV_client_data(basket: Basket):
    '''
    This function should be replaced by a database query or 
    any other source data loading.
    '''

    # Data file path
    sets_column = 'pedi_id'
    items_column = 'prod_id'
    description_column = 'prod_descricao'
    
    filename = 'company_sample.xlsx'
    datapath = getcwd() + '/data/' + filename
    
    df = read_data_from_file(datapath, sets_column, items_column)
    
    basket_mask = df[sets_column].isin(basket.items)
    df = df[basket_mask]

    return sets_column, items_column, description_column, df

def get_client_data(basket: Basket):
    return demo_client_data(basket) if basket.is_demo else SV_client_data(basket)
