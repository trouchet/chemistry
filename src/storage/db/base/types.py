from __future__ import annotations

from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID, NUMERIC
from sqlalchemy import (
    String, 
    Integer
)
from sqlalchemy.types import Union
from typing import TypeVar


# Types
PrimaryKeyType: Union[str, int, UUID] = Union(String, Integer, UUID(as_uuid=True))
Decimal = NUMERIC(precision=10, scale=2)

Base = declarative_base()

# Repository types
PrimaryKeyType = Union[int, str, UUID]
Model = TypeVar("Model", bound=Base)
