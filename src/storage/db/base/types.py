from __future__ import annotations

from typing_extensions import (
    Annotated,
    Union,
    TypeVar
)
from sqlalchemy.dialects.postgresql import UUID, NUMERIC
from uuid import UUID

from .. import Base

# Types
PrimaryKeyType = Union[str, int, UUID]
Decimal = NUMERIC(precision=10, scale=2)

# Generic type for model
ModelType = TypeVar("ModelType", bound=Base)
