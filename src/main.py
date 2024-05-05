from uvicorn import run

from src.app import app
from . import settings, logger

# Run the applications
if __name__ == "__main__":
    # Run the FastAPI application
    run(app, host=settings.APP_HOST, port=settings.APP_PORT)

    # Log the application URL
    message=f"App running on http://{settings.APP_HOST}:{settings.APP_PORT}"    
    logger.info(message)
