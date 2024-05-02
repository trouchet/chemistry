from pydantic import BaseModel

from ..database.utils import sqlalchemy_to_pydantic
from ..database.schemas import Provider
from .utils.security import (
    is_password_strong_dict,
    is_password_strong
)

# Response model
class ErrorResponse(BaseModel):
    error: str

class WeakPasswordException(Exception):
    error: str = "Password does not meet security requirements."
    requirements: dict = {
        "min_length": 8,
        "min_uppercase": 1,
        "min_lowercase": 1,
        "min_digits": 1,
        "min_special_chars": 1,
    }

    def __init__(self, password: str):
        super().__init__(self.error)  # Use pre-defined error message
        if not is_password_strong(password):
            self.requirements = is_password_strong_dict(password)

# Response model
class MessageResponse(BaseModel):
    message: str

# Providers request model
ProvidersPydanticModel = sqlalchemy_to_pydantic(Provider)
class ProviderRequestModel(ProvidersPydanticModel):
    pass
