from pydantic import BaseModel
from typing import List

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str = None

# Request model
class BasketRequest(BaseModel):
    basket: List[str]

# Response model
class RecommendationResponse(BaseModel):
    recommendation: str