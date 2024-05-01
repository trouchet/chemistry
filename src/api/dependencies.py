from collections.abc import Callable

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import schemas
from src.database import session
from src.database.base.repository import DatabaseRepository

def get_repository(
    model: type[schemas.Base],
) -> Callable[[AsyncSession], DatabaseRepository]:
    def func(session: AsyncSession = Depends(session.get_db_session)):
        return DatabaseRepository(model, session)

    return func