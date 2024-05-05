from loguru import logger

# Configure the root logger with rotation and timestamped filenames
logger.add(
    '/tmp/loginfo.log',
    level="DEBUG",
    rotation="50 MB",
    compression="zip",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
)
