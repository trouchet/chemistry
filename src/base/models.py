from pydantic import BaseModel, ConfigDict
from functools import partial

from src.utils.misc import snake2camel

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


# Response model
class MessageResponse(BaseModel):
    message: str