from fastapi import FastAPI, HTTPException

from src.routes import setup, auth, recommendation

def create_app():
    app_ = FastAPI()
    
    app_.include_router(
        setup.router, 
        prefix="/api", tags=["setup"]
    )
    app_.include_router(
        setup.router, 
        prefix="/api", tags=["setup"]
    )
    app_.include_router(
        auth.router, prefix="/api"
    )
    app_.include_router(
        recommendation.router, 
        prefix="/api/recommendation", tags=["recommendation"]
    )

    return app_
