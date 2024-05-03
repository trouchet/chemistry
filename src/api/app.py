# Descrição: Este arquivo é responsável por criar 
# a instância do aplicativo FastAPI e adicionar as rotas a ele.

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.api.endpoints import setup, recommendation, file, signup
from src.db.schemas import Base
from src.db.engine import engine
from src.db.utils import create_db_and_tables
from src.core.config import settings

def create_app():
    app_ = FastAPI(
        title=settings.PROJECT_NAME,
        docs_url="/api/docs",
        openapi_url="/api/openapi.json",
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

@app.on_event("startup")
async def on_startup():
    # Crie o banco de dados e as tabelas
    Base.metadata.create_all(bind=engine)