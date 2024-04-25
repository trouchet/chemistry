from pydantic import BaseModel, Field
import uuid

class Payload(BaseModel):
    """Payload model."""

    pk: uuid.UUID

    class Config:
        """Config class."""

        orm_mode = True
