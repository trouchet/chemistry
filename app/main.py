from fastapi import FastAPI, HTTPException
from apscheduler.schedulers.background import BackgroundScheduler

from app.core.recommendation.models import RecommendationResponse, BasketRequest

# Initialize the app
app = FastAPI()

# Initialize the scheduler
scheduler = BackgroundScheduler()
scheduler.start()

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

# Sample product recommendation logic
def recommend_product(basket):
    # Your recommendation logic here, e.g., return the first item in the basket
    if basket:
        return [42]
    else:
        return []

@app.post("/cesta/sugerir", response_model=RecommendationResponse, status_code=200)
async def recomendar_produto(request: BasketRequest):
    recommendation = recommend_product(request.basket)
    return {"recommendation": recommendation}

# Handle validation errors
@app.exception_handler(HTTPException)
async def validation_exception_handler(request, exc):
    return {"detail": exc.detail}

# Handle unexpected errors
@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    return {"detail": "Internal server error"}
