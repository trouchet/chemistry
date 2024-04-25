# Description: This file is responsible for creating the
# FastAPI app instance and adding the routes to it.
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.routes import setup, auth, recommendation, file


def create_app():
    app_ = FastAPI()

    # Routers
    app_.include_router(setup.router)
    app_.include_router(auth.router)
    app_.include_router(recommendation.router)
    app_.include_router(file.router)

    # Middlewares
    app_.add_middleware(CORSMiddleware)

    return app_


# Get the number of applications from the environment variable
app = create_app()
