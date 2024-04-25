from os import path, getcwd
from fastapi.responses import JSONResponse

from src.api.utils.dataframe import read_data_from_file
from src.api.core.recommendation.schemas import Basket
from src.api.utils.dataframe import get_itemsets_with_items


def make_json_response(status_: int, content_: dict) -> JSONResponse:
    '''
    Descrição: Retorna uma resposta JSON com o código de status e conteúdo especificados.
    Parâmetros:
        status_ (int): O código de status da resposta.
        content_ (dict): O conteúdo da resposta em formato de dicionário.
    Retorna:
        JSONResponse: Uma resposta JSON com o código de status e conteúdo especificados.
    '''
    return JSONResponse(status_code=status_, content=content_)

def make_error_response(content_: dict):
    '''
    Descrição: Retorna uma resposta de erro com o conteúdo especificado.

    Parâmetros:
        content_ (dict): O conteúdo da resposta em formato de dicionário.

    Retorna:
        JSONResponse: Uma resposta de erro com o conteúdo especificado.
    '''
    return make_json_response(400, content_)

def demo_client_data(basket: Basket):
    '''
    Descrição: Esta função é um carregador de dados de demonstração.
    Parâmetros:
        basket (Basket): O objeto da cesta que contém informações sobre a demonstração.
    Retorna:
        Uma tupla contendo o nome das colunas para conjuntos, itens e descrição, juntamente com um DataFrame filtrado.
    '''

    sets_column = 'itemset_id'
    items_column = 'item_id'
    description_column = 'item_description'

    # Data file path
    filename = f'{basket.demo_type}_order_sample.xlsx'
    foldername = 'data'
    filepath = path.join(getcwd(), foldername, filename)

    df = read_data_from_file(filepath)
    
    # Filter the dataframe by the basket items
    order = basket.model_dump()["items"]

    df = get_itemsets_with_items(df, order, sets_column, items_column)

    return sets_column, items_column, description_column, df


# NOTE: Replace this function by database query or any source data loading
def retrieve_data(basket: Basket):
    '''
    Descrição: Esta função deve ser substituída por uma consulta ao banco de dados 
    ou qualquer outra fonte de carregamento de dados.
    Parâmetros:
        basket (Basket): O objeto da cesta que contém informações sobre a consulta de dados.
    Exceção:
        NotImplementedError: Lançada quando a função não está implementada.
    '''
    raise NotImplementedError('This function is not implemented yet.')


def get_client_data(basket: Basket):
    '''
    Descrição: Retorna os dados do cliente, seja dos dados de demonstração ou da consulta de dados, 
    dependendo do tipo de cesta.
    Parâmetros:
        basket (Basket): O objeto da cesta que contém informações sobre a consulta de dados.
    Retorna:
        Os dados do cliente obtidos da função de demonstração ou da consulta de dados, dependendo 
        do tipo de cesta.
    '''
    return demo_client_data(basket) if basket.is_demo else retrieve_data(basket)
