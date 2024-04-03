import pandas as pd
from numpy import unique
from os import path, listdir  
from timy import timer

def listify_items(
    df_: pd.DataFrame,
    sets_column: str,
    items_column: str
):
    result = df_.groupby(sets_column)[items_column] \
               .apply(list) \
               .reset_index(name='items_list')

    return list(result['items_list'])

def get_descriptions(
    df_: pd.DataFrame,
    item_column: str,
    description_column: str
):
    # Drop duplicates based on 'item_column' and keep the first description
    unique_df = df_.drop_duplicates(subset=item_column, keep='first')
    
    # Create a dictionary mapping items to descriptions
    return dict(zip(unique_df[item_column], unique_df[description_column]))

def get_years(
    df_: pd.DataFrame,
    date_column: str
):
    return list(unique(list(pd.to_datetime(df_[date_column]).dt.year)))

def get_unique_elements(
    df_: pd.DataFrame,
    column_label: str
):
    return list(unique(list(df_[column_label])))

def read_data_from_file(filepath: str, sets_column: str, items_column: str) -> pd.DataFrame:
    get_extension = lambda x: x.split('.')[-1]
    extension = get_extension(filepath)

    if extension == 'xlsx':
        df = pd.read_excel(filepath)
    elif extension == 'csv':
        df = pd.read_csv(filepath)
    else:
        raise ValueError(f'Unsupported extension: {extension}')
    
    df = df.dropna()
    relevant_columns = [sets_column, items_column]
    filtered_df = df.groupby(relevant_columns).first().reset_index()
    return filtered_df


def read_data_to_dataframe_gen(
    data_folder_: str,
    sets_column: str,
    items_column: str,
    extension: str = 'xlsx'
):
    filepaths = [
        path.join(data_folder_, filename) 
        for filename in listdir(data_folder_) 
        if filename.split('.')[-1] == extension
    ]
    
    for filepath in filepaths:
        df_ = read_data_from_file(filepath, sets_column, items_column)
        yield filepath, df_

@timer()
def read_data_to_dataframe(
    data_folder_: str,
    sets_column: str,
    items_column: str,
    extension: str = 'xlsx'
):
    return dict(
        read_data_to_dataframe_gen(
            data_folder_, sets_column, items_column, extension
        )
    )