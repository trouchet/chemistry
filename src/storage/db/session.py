from typing import AsyncGenerator
from sqlalchemy import exc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from src.db.engine import create_async_database_engine

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Yields an asynchronous session for database interactions.

    This function is an asynchronous generator that creates a new session using
    the globally defined session factory (likely defined in src.db.engine).

    Yields:
        AsyncSession: An asynchronous session object for interacting with the database.
    """

    async with await create_async_database_engine() as engine:          
        async with sessionmaker(
            autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
        )() as session:
            try:
                yield session
                await session.commit()
            except exc.SQLAlchemyError:
                await session.rollback()
                raise
            finally:
                await session.close()
