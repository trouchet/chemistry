import sys
import logging
import watchdog

# Configure logging to write to stderr
logging.basicConfig(level=logging.DEBUG, stream=sys.stderr)

# Create a logger for the watchdog module
watchdog_logger = logging.getLogger('watchdog')

# Set the logging level for the watchdog logger
watchdog_logger.setLevel(logging.ERROR)

