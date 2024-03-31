from src.logging import logging

# Function to be executed as a scheduled task
def print_statement():
    logging.debug("Scheduled task: Hello, World!")
