from sqlalchemy.orm import declarative_base

# model base class
Base = declarative_base()

from .schemas import User

from .exceptions import (
    InvalidEmailException,
    UserNotFoundException,
    UserAlreadyExistsException,
)