from prometheus_fastapi_instrumentator import Instrumentator
from uvicorn import run

from src.scheduler.scheduler import scheduler
from src.app import app
from src.setup.config import settings

# Start Prometheus logging metrics
prometheus_intrumentator=Instrumentator()
prometheus_intrumentator.instrument(app)
prometheus_intrumentator.expose(app)

# Start the scheduler
scheduler.start()

# Run the applications
if __name__ == "__main__":
    run(app, host=settings.APP_HOST, port=settings.APP_PORT)
