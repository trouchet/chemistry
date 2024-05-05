from prometheus_fastapi_instrumentator import Instrumentator
from src.scheduler.scheduler import scheduler

# Start Prometheus logging metrics
prometheus_intrumentator=Instrumentator()
prometheus_intrumentator.instrument(app)
prometheus_intrumentator.expose(app)

# Start the scheduler
scheduler.start()