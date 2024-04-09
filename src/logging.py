import logging
from logstash_formatter import LogstashFormatterV1
from logging.handlers import SocketHandler

from os import environ
from dotenv import load_dotenv

load_dotenv()

LOGSTASH_HOST = environ.get('LOGSTASH_HOST')
LOGSTASH_PORT = environ.get('LOGSTASH_PORT')

# Configure the root logger
logger = logging.getLogger('gunicorn.error')

# Configure a handler to send logs to Logstash
handler = SocketHandler(LOGSTASH_HOST, int(LOGSTASH_PORT))

formatter = LogstashFormatterV1()
handler.setFormatter(formatter)

logger.addHandler(handler)
