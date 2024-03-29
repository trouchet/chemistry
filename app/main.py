from fastapi import FastAPI, HTTPException
from apscheduler.schedulers.background import BackgroundScheduler

from app.core.recommendation.models import RecommendationResponse, BasketRequest
from app.services.

# Initialize the app
app = FastAPI()

# Initialize the scheduler
scheduler = BackgroundScheduler()
scheduler.start()

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

# Handle validation errors
@app.exception_handler(HTTPException)
async def validation_exception_handler(request, exc):
    return {"detail": exc.detail}

# Handle unexpected errors
@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    return {"detail": "Internal server error"}
