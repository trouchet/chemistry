from typing import AsyncGenerator, AsyncIterator, Dict, Any
from sqlmodel import Session, create_engine, select
from collections.abc import Generator

import contextlib

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncSession
)
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    create_engine,
)

from backend.app.db.models.users import User, UserCreate
from backend.app.api.services.users import create_user 
from backend.app import settings

# Heavily inspired by 
# https://praciano.com.br/fastapi-and-async-sqlalchemy-20-with-pytest-done-right.html


engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)

def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


def init_db(session: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next lines
    # from sqlmodel import SQLModel

    # from app.core.engine import engine
    # This works because the models are already imported and registered from app.models
    # SQLModel.metadata.create_all(engine)

    user = session.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = create_user(session=session, user_create=user_in)