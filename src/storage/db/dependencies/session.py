from typing_extensions import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.storage.db.base.manager import get_db_session

DatabaseSessionDependency = Annotated[AsyncSession, Depends(get_db_session)]

