import threading
from prometheus_fastapi_instrumentator import Instrumentator
from uvicorn import run

from api.setup.scheduler import scheduler
from api.app import app

# Start Prometheus logging metrics
Instrumentator().instrument(app).expose(app)


# Start the scheduler in a separate thread
def start_scheduler():
    scheduler.start()


scheduler_thread = threading.Thread(target=start_scheduler)
scheduler_thread.daemon = True
scheduler_thread.start()

# Run the application
if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8000)
