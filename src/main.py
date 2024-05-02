from prometheus_fastapi_instrumentator import Instrumentator
from fastapi import HTTPException
from uvicorn import run

from src.api.setup.scheduler import scheduler
from src.api.app import app
from src.core import settings

# Start Prometheus logging metrics
Instrumentator().instrument(app).expose(app)

# Start the scheduler
scheduler.start()

# Run the applications
if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8000)
