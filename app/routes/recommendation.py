from fastapi import APIRouter

from app.core.recommendation.models import RecommendationResponse, \
    BasketRequest

router = APIRouter()

# Sample product recommendation logic
def recommend_product(basket):
    # Your recommendation logic here, e.g., return the first item in the basket
    if basket:
        return [42]
    else:
        return []

@router.post(
    "/basket", 
    response_model=RecommendationResponse, 
    status_code=200
)
async def recomendar_produto(request: BasketRequest):
    recommendation = recommend_product(request.basket)
    return {"recommendation": recommendation}