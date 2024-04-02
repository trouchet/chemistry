from prometheus_fastapi_instrumentator import Instrumentator

from uvicorn import run
from src.app import app
from src.scheduler import scheduler

# Start Prometheus logging metrics
Instrumentator().instrument(app).expose(app)

# # Start the scheduler
# scheduler.start()

'''
from fastapi_jwt_auth import AuthJWT

# callback to get your configuration
@AuthJWT.load_config
def get_config():
    return Settings()
'''

# Run the applications
if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8000)
