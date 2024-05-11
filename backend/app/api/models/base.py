from pydantic import BaseModel


# Response model
class MessageResponse(BaseModel):
    message: str
