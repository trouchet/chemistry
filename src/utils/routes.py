from os import path
from fastapi.responses import JSONResponse

from src.utils.dataframe import read_data_from_file
from src.core.recommendation.models import Basket
from src.utils.dataframe import get_itemsets_with_items


def make_json_response(status_: int, content_: dict) -> JSONResponse:
    return JSONResponse(status_code=status_, content=content_)

def demo_client_data(basket: Basket):
    '''
    This function is a demo data loader.
    '''
    from os import getcwd

    sets_column = 'order_id'
    items_column = 'item_id'
    description_column = 'description'

    # Data file path
    filename = f'{basket.demo_type}_test_sample.xlsx'
    foldername = 'data'
    filepath = path.join(getcwd(), foldername, filename)         

    df = read_data_from_file(filepath, sets_column, items_column)
    
    # Filter the dataframe by the basket items
    order = basket.model_dump()["items"]

    df = get_itemsets_with_items(df, order, sets_column, items_column)

    return sets_column, items_column, description_column, df


# NOTE: Replace this function by database query or any source data loading
def client_data(basket: Basket):
    raise NotImplementedError('This function is not implemented yet.')


def get_client_data(basket: Basket):
    return demo_client_data(basket) \
        if basket.is_demo \
        else client_data(basket)
