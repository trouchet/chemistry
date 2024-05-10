from pydantic import BaseModel, ConfigDict
from functools import partial

from backend.app.api.utils.native import snake2camel
from sqlmodel import Field, Relationship, SQLModel


class APIModel(BaseModel):
    """
    Intended for use as a base class for externally-facing models.
    Any models that inherit from this class will:
    * accept fields using snake_case or camelCase keys
    * use camelCase keys in the generated OpenAPI spec
    """
    model_config = ConfigDict(
        populate_by_alias = True,
        alias_generator = partial(snake2camel, start_lower=False),
    )

# Response model
class MessageResponse(APIModel):
    message: str
    
