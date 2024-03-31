from fastapi import FastAPI, HTTPException

from src.routes import setup, \
    security, \
    monitoring, \
    recommendation

def create_app(index_: int):
    app_ = FastAPI()
    
    @app_.get(f"/app{index_+1}")
    async def route_app():
        return {"message": f"Hello from App {index_+1}"}

    # Routes: Extend this for more routes
    app_.include_router(
        monitoring.router, tags=['monitoring']
    )
    
    app_.include_router(
        setup.router, 
        prefix="/api", tags=["setup"]
    )
    app_.include_router(
        security.router, 
        prefix="/api"
    )
    app_.include_router(
        recommendation.router, 
        prefix="/api/recommendation", tags=["recommendation"]
    )

    # Exception handlers
    @app_.exception_handler(HTTPException)
    async def validation_exception_handler(request, exc):
        return {"detail": exc.detail}

    @app_.exception_handler(Exception)
    async def generic_exception_handler(request, exc):
        return {"detail": "Internal server error"}

    return app_