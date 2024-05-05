# Descrição: Este arquivo é responsável por criar
# a instância do aplicativo FastAPI e adicionar as rotas a ele.

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from prometheus_fastapi_instrumentator import Instrumentator
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from src.setup.config import settings
from src.routes import setup, file, signup
from src.db.engine import (
    create_async_database_engine, 
    Base
)
from src.db.utils import create_db_and_tables

from src.api.scheduler.scheduler import scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with await create_async_database_engine() as engine:
        # Create tables or perform other database operations
        await create_db_and_tables(engine)

        # Create session factory within transaction for better resource management
        async_session_local = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine,
            expire_on_commit=False,
            class_=AsyncSession,
        )
        
        try:
            yield async_session_local
        finally:
            await async_session_local.close() 


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
    app_.include_router(signup.router)
    app_.include_router(file.router)

    # Add middlewares here
    app_.add_middleware(CORSMiddleware)

    return app_


# Get the number of applications from the environment variable
app = create_app()

def setup_app(app):
    # Start Prometheus logging metrics
    prometheus_intrumentator=Instrumentator()
    prometheus_intrumentator.instrument(app)
    prometheus_intrumentator.expose(app)

    # Start the scheduler
    scheduler.start()

    return app