from loguru import logger
from os import environ
import logging
from logging.handlers import SocketHandler

LOGSTASH_HOST = environ.get('LOGSTASH_HOST', 'localhost')
LOGSTASH_PORT = int(environ.get('LOGSTASH_PORT', 5959))

# Configure the Logstash handler
logstash_handler = SocketHandler(LOGSTASH_HOST, LOGSTASH_PORT)
logstash_handler.setLevel(logging.INFO)

# Add the Logstash handler to the logger
logger.add(logstash_handler)

# Log some messages
logger.info("[TEST] Logging with Loguru and sending to Logstash")
logger.warning("[TEST] This is a warning message")
logger.error("[TEST] This is an error message")