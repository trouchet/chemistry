# taken from here https://github.com/dmontagu/fastapi-utils
from pydantic import ConfigDict, BaseModel
from fastapi import HTTPException
from functools import partial

from .utils.security import is_password_strong_dict
from src.api.utils.misc import snake2camel


class APIModel(BaseModel):
    """
    Intended for use as a base class for externally-facing models.
    Any models that inherit from this class will:
    * accept fields using snake_case or camelCase keys
    * use camelCase keys in the generated OpenAPI spec
    """

    class Config(ConfigDict):
        populate_by_name = True
        alias_generator = partial(snake2camel, start_lower=True)


# Response model
class ErrorResponse(BaseModel):
    error: str


class WeakPasswordException(HTTPException):
    error: str = ""

    def __init__(self, password: str):
        super().__init__(self.error)  # Use pre-defined error message

        # Password validation
        password_check_dict = is_password_strong_dict(password)

        self.error = f"Password does not meet security requirements. Check it out: {password_check_dict}."


# Response model
class MessageResponse(BaseModel):
    message: str


# Providers request model
class ProviderRequestModel(BaseModel):
    username: str
    password: str
