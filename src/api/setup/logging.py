from os import path
import time
from loguru import logger


def get_log_filename():
    """
    Creates a unique filename with a timestamp for log files.

    Returns:
        str: The formatted filename with a timestamp (YYYY-MM-DD_HH-MM-SS.log).
    """
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    return path.join("logs", f"{timestamp}.log")


# Configure the root logger with rotation and timestamped filenames
logger.add(
    'loginfo.log',
    level="DEBUG",
    rotation="50 MB",
    compression="zip",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
)
