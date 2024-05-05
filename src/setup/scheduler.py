# Description: This file is used to set up the scheduler for the application.
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from apscheduler.triggers.interval import IntervalTrigger

from src.api.tasks.recommendation_task import generate_recommendations

from src.api.tasks.logs_clean_task import manage_files_periodically

from src.api.tasks.print_task import print_statement

# Initialize the scheduler
scheduler = BackgroundScheduler()

# Test task: Add the scheduled task with a 1 minute interval
interval_1_s = IntervalTrigger(seconds=5)
scheduler.add_job(print_statement, trigger=interval_1_s)

# Production task: Add the scheduled task to trigger at midnight
trigger_midnight = CronTrigger(hour=0, minute=0)
scheduler.add_job(generate_recommendations, trigger=trigger_midnight)

# Production task: Add the scheduled task to manage log files at midnight
scheduler.add_job(manage_files_periodically, trigger=trigger_midnight)
