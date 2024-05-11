from backend.app.core.logging import logger


# Function to be executed as a scheduled task
def print_statement():
    logger.debug("Scheduled task: Hello, World!")
