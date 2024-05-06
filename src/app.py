# Descrição: Este arquivo é responsável por criar
# a instância do aplicativo FastAPI e adicionar as rotas a ele.

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from contextlib import asynccontextmanager

from . import settings
from src.scheduler.schedule import scheduler
from src.routes import auth, setup, file
from src.storage.db.base.manager import session_manager
from src.storage.db.utils import create_db_and_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Function that handles startup and shutdown events.
    To understand more, read https://fastapi.tiangolo.com/advanced/events/
    """
    await create_db_and_tables()

    yield
    if session_manager._engine is not None:
        # Close the DB connection
        await session_manager.close()


def create_app():
    # Generates the FastAPI application
    app_ = FastAPI(
        title=settings.PROJECT_NAME,
        docs_url="/api/docs",
        openapi_url="/api/openapi.json",
        lifespan=lifespan,
    )

    # Add routers here
    app_.include_router(setup.router)
    app_.include_router(auth.router)
    app_.include_router(file.router)

    # Add middlewares here
    app_.add_middleware(CORSMiddleware)

    return app_


def setup_app(app_):
    """
    Setup the application with the necessary configurations.

    Args:
        app_ (FastAPI): FastAPI application instance

    Returns:
        FastAPI: FastAPI application instance with the necessary configurations
    """
    # Start Prometheus logging metrics
    prometheus_intrumentator=Instrumentator()
    prometheus_intrumentator.instrument(app_)
    prometheus_intrumentator.expose(app_)

    # Start the scheduler
    scheduler.start()

    return app_


# Get the number of applications from the environment variable
app = create_app()

# Setup the application
app = setup_app(app)

