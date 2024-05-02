from sqlalchemy.ext.declarative import DeclarativeMeta
from pydantic import BaseModel
from typing import Type, TypeVar

T = TypeVar("T")
from sqlalchemy import Column

def sqlalchemy_to_pydantic(model: DeclarativeMeta) -> Type[T]:
    """
    Convert a SQLAlchemy model to a Pydantic model.

    Args:
        model (DeclarativeMeta): SQLAlchemy model to convert.

    Returns:
        type(BaseModel): Pydantic model equivalent to the SQLAlchemy model.
    """
    class PydanticModel(BaseModel):
        class Config:
            from_attributes = True

    for column_name in model.__table__.columns.keys():
        column = getattr(model, column_name)
        if isinstance(column, Column):
            PydanticModel.__annotations__[column_name] = (column.type.python_type, None)

    return PydanticModel
