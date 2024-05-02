from pydantic import BaseModel

from src.models.api_model import APIModel

class Token(APIModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: str
    exp: int