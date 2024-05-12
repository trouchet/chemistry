from sqlmodel import Session, create_engine, select
from typing import Generator
from sqlmodel import SQLModel

from ..models.users import User, UserCreate
from ..api.services.users import create_user
from backend.app.core.config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


def init_db(session: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next lines
    if settings.TESTING:
        SQLModel.metadata.create_all(engine)

    query = select(User).where(User.email == settings.FIRST_SUPERUSER)
    user = session.exec(query).first()

    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )

        user = create_user(session=session, user_create=user_in)
