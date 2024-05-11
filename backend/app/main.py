from uvicorn import run

from backend.app import app, settings, logger

# Run the applications
if __name__ == "__main__":
    # Run the FastAPI application
    run(app, host=settings.APP_HOST, port=settings.APP_PORT)

    # Log the application URL
    logger.info(f"App running on {settings.server_host}")
