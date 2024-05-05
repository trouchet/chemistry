from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.ext.asyncio import AsyncEngine
from pydantic import BaseModel, ConfigDict
from sqlalchemy import Column

from typing import Type, TypeVar

from src.db.engine import Base

T = TypeVar("T")

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


async def create_db_and_tables(engine: AsyncEngine):
    """
    Creates all tables defined using Base in the provided engine.

    Args:
        engine: The asynchronous engine to use for creating tables.
    """
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    

    async with engine.begin() as conn:
        await conn.runsync(Base.metadata.create_all())


async def drop_db_and_tables(engine):
    """
    Drops all tables defined using Base in the provided engine.

    Args:
        engine: The asynchronous engine to use for dropping tables.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def recreate_db_and_tables(engine):
    """
    Recreates all tables defined using Base in the provided engine.

    Args:
        engine: The asynchronous engine to use for recreating tables.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
