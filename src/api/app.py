# Descrição: Este arquivo é responsável por criar 
# a instância do aplicativo FastAPI e adicionar as rotas a ele.

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from src.core.config import settings
from src.api.endpoints import setup, recommendation, file, signup
from src.db.engine import raw_database_connection
from src.db.engine import async_database_engine
from src.db.utils import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    await raw_database_connection.connect()
    await create_db_and_tables(async_database_engine)
    yield
    await raw_database_connection.disconnect()

def create_app():
    # Crie uma instância do aplicativo FastAPI
    app_ = FastAPI(
        title=settings.PROJECT_NAME,
        docs_url="/api/docs",
        openapi_url="/api/openapi.json",
        lifespan=lifespan
    )

    # Adicione as rotas ao aplicativo
    app_.include_router(setup.router)
    app_.include_router(signup.router)
    app_.include_router(recommendation.router)
    app_.include_router(file.router)
    
    app_.add_middleware(CORSMiddleware)

    return app_


# Get the number of applications from the environment variable
app = create_app()
