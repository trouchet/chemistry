# Description: This file contains the function that will 
# be executed as a scheduled task
from src.setup.logging import logging


# Function to be executed as a scheduled task
def print_statement():
    logging.debug("Scheduled task: Hello, World!")
