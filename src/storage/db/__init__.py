from sqlalchemy.orm import declarative_base

# model base class
Base = declarative_base()

from .schemas import User

from .exceptions import (
    InvalidEmailException,
    UserNotFoundException,
)

from .utils import (
    create_db_and_tables,
    drop_db_and_tables,
    recreate_db_and_tables,
)