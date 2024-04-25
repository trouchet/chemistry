import pandas as pd
from numpy import unique
from os import path, listdir
from timy import timer
from typing import List


def listify_items(df_: pd.DataFrame, sets_column: str, items_column: str) -> List[list]:
    '''
    - Agrupa os itens de cada conjunto em uma lista.
    - Parâmetros:
        - `df_`: DataFrame contendo os dados.
        - `sets_column`: Nome da coluna que contém os conjuntos.
        - `items_column`: Nome da coluna que contém os itens.
    - Retorna uma lista dos conjuntos, onde cada conjunto é uma lista de itens.
    '''

    result = (
        df_.groupby(sets_column)[items_column]
        .apply(list)
        .reset_index(name='items_list')
    )

    return list(result['items_list'])


def get_itemsets_with_items(
    df_: pd.DataFrame, 
    items_list: list, 
    sets_column: str, 
    items_column: str
) -> pd.DataFrame:  
    '''
    - Filtra os conjuntos que contêm pelo menos um dos itens fornecidos.
    - Parâmetros:
        - `df_`: DataFrame contendo os dados.
        - `items_list`: Lista de itens a serem verificados nos conjuntos.
        - `sets_column`: Nome da coluna que contém os conjuntos.
        - `items_column`: Nome da coluna que contém os itens.
    - Retorna um DataFrame contendo apenas os conjuntos que contêm pelo menos um dos itens fornecidos.
    '''
    
    def mask_map(group: pd.Series) -> bool:
        is_empty = group[items_column].empty
        has_intersection = set(group[items_column]).intersection(items_list)
        return not is_empty and len(has_intersection) > 0
    
    grouped_df = df_.groupby(sets_column)
    return grouped_df.filter(mask_map)


def get_descriptions(
    df_: pd.DataFrame, 
    item_column: str, 
    description_column: str
) -> dict:  
    '''
    - Obtém um dicionário que mapeia cada item à sua descrição correspondente.
    - Parâmetros:
        - `df_`: DataFrame contendo os dados.
        - `item_column`: Nome da coluna que contém os itens.
        - `description_column`: Nome da coluna que contém as descrições.
    - Retorna um dicionário com os itens como chaves e as descrições como valores.
    '''
    # Drop duplicates based on 'item_column' and keep the first description
    unique_df = df_.drop_duplicates(subset=item_column, keep='first')

    # Create a dictionary mapping items to descriptions
    return dict(zip(unique_df[item_column], unique_df[description_column]))


def get_years(df_: pd.DataFrame, date_column: str) -> List[int]:
    return list(unique(list(pd.to_datetime(df_[date_column]).dt.year)))


def get_unique_elements(df_: pd.DataFrame, column_label: str) -> List[str]:
    return list(unique(list(df_[column_label])))


def read_data_from_file(
    filepath: str
) -> pd.DataFrame:
    def get_extension(word: str):
        return word.split('.')[-1]

    extension = get_extension(filepath)

    if extension in ['xlsx', 'xls']:
        df = pd.read_excel(filepath, engine='openpyxl')
    elif extension == 'csv':
        df = pd.read_csv(filepath)
    else:
        raise ValueError(f'Unsupported extension: {extension}')

    return df


def read_data_to_dataframe_gen(
    data_folder_: str, extension: str = 'xlsx'
) -> dict:
    filepaths = [
        path.join(data_folder_, filename)
        for filename in listdir(data_folder_)
        if filename.split('.')[-1] == extension
    ]

    for filepath in filepaths:
        df_ = read_data_from_file(filepath)
        yield filepath, df_


@timer()
def read_data_to_dataframe(
    data_folder_: str, sets_column: str, items_column: str, extension: str = 'xlsx'
) -> dict:
    return dict(
        read_data_to_dataframe_gen(data_folder_, sets_column, items_column, extension)
    )
