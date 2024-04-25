# Description: Configure the root logger to send logs to Logstash
import logging
from logging.handlers import SocketHandler

from os import environ
from dotenv import load_dotenv

load_dotenv()

# Configure the root logger
logger = logging.getLogger('gunicorn.error')

# Set the log level
logger.setLevel(logging.INFO)
