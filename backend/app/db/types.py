from __future__ import annotations

from pydantic import (
    field_validator, 
    Field, 
    UUID4
)
from typing_extensions import (
    Union,
    TypeVar,
)

from sqlalchemy.dialects.postgresql import UUID, NUMERIC
from datetime import datetime

# Types
Decimal = NUMERIC(precision=10, scale=2)

# Generic type for model
ModelType = TypeVar("ModelType", bound=Base)

# Primary type for primary key
PrimaryKeyType = Union[UUID4, int, str]

def get_current_timestamp():
    return datetime.now()

class DatetimeTypeMixin:
    created_at: datetime = Field(
        index=True, default=get_current_timestamp
    )
    updated_at: datetime = Field(
        index=True, default=get_current_timestamp
    )

    @field_validator("created_at")
    @classmethod
    def validate_created_at(cls, created_at):
        return created_at

    @field_validator("updated_at")
    @classmethod
    def validate_updated_at(cls, updated_at):
        return updated_at

    @classmethod
    def get_current_timestamp(cls):
        return get_current_timestamp()

    @classmethod
    def get_current_timestamp(cls):
        return get_current_timestamp()