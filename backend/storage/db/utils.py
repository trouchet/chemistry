from sqlalchemy.ext.asyncio import AsyncEngine

from typing import TypeVar
from backend.storage.db import Base

T = TypeVar("T")

async def create_db_and_tables(engine: AsyncEngine):
    """
    Creates all tables defined using Base in the provided engine.

    Args:
        engine: The asynchronous engine to use for creating tables.
    """
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    

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
