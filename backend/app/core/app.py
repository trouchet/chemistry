# Descrição: Este arquivo é responsável por criar
# a instância do aplicativo FastAPI e adicionar as rotas a ele.

import sentry_sdk
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from fastapi.routing import APIRoute

from .. import settings
from ..scheduler.schedule import scheduler

from ..api.main import api_router

if settings.SENTRY_DSN and settings.ENVIRONMENT != "local":
    sentry_sdk.init(dsn=str(settings.SENTRY_DSN), enable_tracing=True)


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


def create_app():
    # Generates the FastAPI application
    app_ = FastAPI(
        title=settings.PROJECT_NAME,
        docs_url=f"{settings.API_V1_STR}/docs",
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        generate_unique_id_function=custom_generate_unique_id,
    )

    return app_


def setup_app(app_):
    """
    Setup the application with the necessary configurations.

    Args:
        app_ (FastAPI): FastAPI application instance

    Returns:
        FastAPI: FastAPI application instance with the necessary configurations
    """
    # Add routers here
    app_.include_router(api_router, prefix=settings.API_V1_STR)

    # Set all CORS enabled origins
    if settings.BACKEND_CORS_ORIGINS:
        app_.add_middleware(
            CORSMiddleware,
            allow_origins=[
                str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS
            ],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Start Prometheus logging metrics
    prometheus_intrumentator = Instrumentator()
    prometheus_intrumentator.instrument(app_)
    prometheus_intrumentator.expose(app_)

    return app_


# Get the number of applications from the environment variable
app = create_app()

# Setup the application
app = setup_app(app)

# Start the scheduler
scheduler.start()
