from sqlalchemy import (
    Column, 
    String, 
    DateTime
)
from sqlalchemy.types import Union, UUID
from pydantic.functional_validators import field_validator
from email_validator import validate_email, EmailNotValidError
from src.db.engine import Base

from datetime import now

def get_current_timestamp():
    return now()

class User(Base):
    """
    User model for the database.
    """
    __tablename__ = "users"

    id = Column(
        UUID, primary_key=True, index=True, 
        comment='Primary key on database for user'
    )
    signed_up_at = Column(
        DateTime, default=get_current_timestamp,
        comment='Datetime when the user was registered',
    )
    username = Column(String, nullable=False, unique=True, comment='Service username')
    email = Column(String, nullable=False, unique=True, comment='User email', )
    hashed_password = Column(String, nullable=False, comment='Hashed user password')
    token_str = Column(String, nullable=False, comment='Access user token')

    @field_validator("email")
    @classmethod
    def validate_email(cls, email):
        try:
            validate_email(email)
        except EmailNotValidError:
            raise ValueError("Invalid email format")
        return email
