# Descrição: Este arquivo é responsável por criar 
# a instância do aplicativo FastAPI e adicionar as rotas a ele.

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.api.endpoints import \
    auth, \
    setup, \
    recommendation, \
    file
from src.database.schemas import Base
from src.database.engine import engine
from core.config import settings

def create_app():
    # Crie o banco de dados e as tabelas
    Base.metadata.create_all(bind=engine)

    app_ = FastAPI(
        title=settings.project_name,
        docs_url="/api/docs",
        openapi_url="/api/openapi.json",
    )

    app_.include_router(setup.router)
    app_.include_router(auth.router)
    app_.include_router(recommendation.router)
    app_.include_router(file.router)
    
    app_.add_middleware(CORSMiddleware)

    return app_


# Get the number of applications from the environment variable
app = create_app()
