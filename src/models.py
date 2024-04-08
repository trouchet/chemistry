from pydantic import BaseModel, Field
from typing import Optional, List
from os import environ

from src.core.recommendation.constants import N_BEST_NEIGHBORS_DEFAULT, \
    RECOMMENDATION_ALGO_DEFAULT

# JWT Secret and Algorithm
JWT_SECRET = str(environ.get('JWT_SECRET'))
JWT_ALGORITHM = str(environ.get('JWT_ALGORITHM')) 
    
# In production, you can use Settings management
# from pydantic to get secret key from .env
class JWTSettings(BaseModel):
    authjwt_secret_key: str = JWT_SECRET
    authjwt_algorithm: str = JWT_ALGORITHM

class User(BaseModel):
    username: str
    password: str

class Resource(BaseModel):
    is_demo: Optional[bool] = True

# Request model
class Item(Resource):
    id: str

# Request model
class Basket(Resource):
    client_id: str = None
    items: List[str] = Field(default=[])
    algorithm: Optional[str] = RECOMMENDATION_ALGO_DEFAULT
    neighbors_count: Optional[int] = N_BEST_NEIGHBORS_DEFAULT
    age_months: Optional[int] = DEFAULT_AGE

    def is_age_valid(self):
        """
        Checks if age_months is within VALID_AGE_MONTHS
        """
        return False \
            if self.age_months is None \
            else self.age_months in VALID_AGE_MONTHS


# Response model
class Recommendation(BaseModel):
    items: Optional[List[str]] = []
    metadata: Optional[dict] = {}

