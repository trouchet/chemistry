from typing import AsyncGenerator
from sqlalchemy import exc
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.engine import SessionLocal


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
        except exc.SQLAlchemyError:
            await session.rollback()
            raise
        finally:
            await session.close()
