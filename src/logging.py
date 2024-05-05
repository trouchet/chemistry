from loguru import logger
from sys import stdout

from . import settings

is_development=settings.ENVIRONMENT == "development"
log_type="DEBUG" if is_development else "INFO"

logger.remove(0)

# Configure the logger to output to the console
logger.add(
    stdout, 
    level=log_type
)

# Configure the root logger with rotation and timestamped filenames
logger.add(
    '/tmp/loginfo.log',
    level=log_type,
    rotation="50 MB",
    compression="zip",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
)
