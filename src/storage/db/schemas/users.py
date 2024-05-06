from sqlalchemy.orm import Mapped, mapped_column
from pydantic import UUID4
from email_validator import validate_email, EmailNotValidError
from pydantic.functional_validators import field_validator
import datetime

from src.storage.db import Base
from src.storage.db.exceptions import InvalidEmailException

def get_current_timestamp():
    return datetime.datetime.now()

class User(Base):
    """
    User model for the database.
    """
    __tablename__ = "users"

    id: Mapped[UUID4] = mapped_column(
        primary_key=True, index=True, 
        comment='Database primary key on database for user'
    )
    signed_up_at: Mapped[datetime.datetime] = mapped_column(
        index=True, default=get_current_timestamp,
        comment='User registered datetime',
    )
    username: Mapped[str] = mapped_column(
        nullable=False, unique=True, 
        comment='Username'
    )
    email: Mapped[str] = mapped_column(
        nullable=False, unique=True, 
        comment='User email'
    )
    hashed_password: Mapped[str] = mapped_column(
        nullable=False, 
        comment='User hashed password'
    )
    token_str: Mapped[str] = mapped_column(
        nullable=False, 
        comment='User access token'
    )

    @field_validator("email")
    @classmethod
    def validate_email(cls, email):
        try:
            validate_email(email)
        except EmailNotValidError:
            raise InvalidEmailException()
        
        return email