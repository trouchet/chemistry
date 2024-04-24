from os import listdir, path, getcwd

from src.setup.logging import logging
from src.constants import datafile_extensions
from src.utils.dataframe import read_data_from_file

# NOTE: The columns are hardcoded for now
dataset_columns = [
    'itemset_timestamp', 
    'itemset_id', 
    'agent_id', 
    'item_id', 
    'item_description', 
    'item_quantity', 
    'item_value'
]

def generate_recommendations():
    logging.debug("Scheduled task: Generating recommendations...")
    data_path = path.join(getcwd(), 'data')
    
    files_list = listdir(data_path)
    
    for file in files_list:
        try:
            filepath = path.join(data_path, file)
            
            read_data_from_file(filepath, dataset_columns)

        except ValueError:
            continue
    
    for file in files_list:
        logging.debug(f"Processing file: {file}")
