from typing import AsyncGenerator, AsyncIterator, Dict, Any
from sqlmodel import Session, create_engine, select
import contextlib

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncSession
)
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from backend import settings

# Heavily inspired by 
# https://praciano.com.br/fastapi-and-async-sqlalchemy-20-with-pytest-done-right.html
class DatabaseSessionManager:
    def __init__(self, uri: str, engine_kwargs: Dict[str, Any] = {}):
        self._engine = create_async_engine(uri, **engine_kwargs)
        self._sessionmaker = async_sessionmaker(
            autocommit=False, autoflush=False, 
            bind=self._engine, class_=AsyncSession
        )

    async def close(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        
        await self._engine.dispose()

        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except SQLAlchemyError:
            await session.rollback()
            raise
        finally:
            await session.close()



# Create a new instance of the DatabaseSessionManager
session_manager = DatabaseSessionManager(settings.SQLALCHEMY_DATABASE_URI)

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Yields an asynchronous session for database interactions.

    This function is an asynchronous generator that creates a new session using
    the provided engine.

    Args:
        engine (AsyncEngine, optional): The asynchronous engine to use for session creation. 
        Defaults to Depends(get_async_engine).

    Yields:
        AsyncSession: An asynchronous session object for interacting with the database.
    """
    async with session_manager.session() as session:
        yield session
    
def init_db() -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next lines
    # from sqlmodel import SQLModel

    # from app.core.engine import engine
    # This works because the models are already imported and registered from app.models
    # SQLModel.metadata.create_all(engine)

    user = session_manager.session.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = crud.create_user(session=session, user_create=user_in)