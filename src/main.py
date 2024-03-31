
from apscheduler.schedulers.background import BackgroundScheduler
from uvicorn import run
from os import getenv 

from src.app_factory import create_app

# Initialize the scheduler
scheduler = BackgroundScheduler()
scheduler.start()

# Get the number of applications from the environment variable
APPS_COUNT = 1 # int(getenv("APPS_COUNT", 1))

# Create a list to store the FastAPI applications
apps = []

# Create and append the FastAPI applications to the list
# for i in range(APPS_COUNT):
#    apps.append(create_app(i))
app = create_app(0)

# Run the applications
# if __name__ == "__main__":
#    for i, app in enumerate(apps, start=1):
#        run(app, host="0.0.0.0", port=8000 + i)
