from uvicorn import run

from backend.app.app import app
from backend.app.core.config import settings
from backend.app.core.logging import logger

# Run the applications
if __name__ == "__main__":
    # Run the FastAPI application
    run(app, host=settings.APP_HOST, port=settings.APP_PORT)

    # Log the application URL
    logger.info(f"App running on {settings.server_host}")
