# Description: This file is responsible for creating the
# FastAPI app instance and adding the routes to it.
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.routes import setup, auth, recommendation
from src.database.engine import Base, engine

def create_app():
    # Crie o banco de dados e as tabelas
    Base.metadata.create_all(bind=engine)

    app_ = FastAPI()

    app_.include_router(setup.router, prefix="/api", tags=["setup"])
    app_.include_router(auth.router, prefix="/api")
    app_.include_router(
        recommendation.router, prefix="/api/recommendation", tags=["recommendation"]
    )

    app_.add_middleware(CORSMiddleware)

    return app_


# Get the number of applications from the environment variable
app = create_app()
