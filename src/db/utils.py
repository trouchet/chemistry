from sqlalchemy.ext.declarative import DeclarativeMeta
from pydantic import BaseModel, ConfigDict
from typing import Type, TypeVar
from sqlalchemy.orm import declarative_base

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
        class Config(ConfigDict):
            from_attributes = True

    for column_name in model.__table__.columns.keys():
        column = getattr(model, column_name)
        if isinstance(column, Column):
            PydanticModel.__annotations__[column_name] = (column.type.python_type, None)

    return PydanticModel


# Create all tables stored in this metadata in the actual file.
Base = declarative_base()


async def create_db_and_tables(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_db_and_tables(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def recreate_db_and_tables(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
