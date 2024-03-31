from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from src.tasks.print_task import print_statement
from src.logging import logging

# Function to be executed as a scheduled task
def print_statement():
    logging.debug("Scheduled task: Hello, World!")

# Initialize the scheduler
scheduler = BackgroundScheduler()

# Add the scheduled task with a five-second interval
interval_1 = IntervalTrigger(seconds=5)
scheduler.add_job(print_statement, trigger=interval_1)
