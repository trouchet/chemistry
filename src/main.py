from prometheus_fastapi_instrumentator import Instrumentator
from uvicorn import run

from src.scheduler import scheduler
from src.app import app

# Start Prometheus logging metrics
Instrumentator().instrument(app).expose(app)

# Start the scheduler
scheduler.start()

# Run the applications
if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8000)
