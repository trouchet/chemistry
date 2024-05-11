from typing_extensions import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ...db.base import get_db

DatabaseSessionDependency = Annotated[AsyncSession, Depends(get_db)]
