# taken from here https://github.com/dmontagu/fastapi-utils
from functools import partial

from pydantic import ConfigDict
from pydantic import BaseModel

from src.utils.camelcase import snake2camel


class APIModel(BaseModel):
    """
    Intended for use as a base class for externally-facing models.
    Any models that inherit from this class will:
    * accept fields using snake_case or camelCase keys
    * use camelCase keys in the generated OpenAPI spec
    """

    class Config(ConfigDict):
        allow_population_by_field_name = True
        alias_generator = partial(snake2camel, start_lower=True)