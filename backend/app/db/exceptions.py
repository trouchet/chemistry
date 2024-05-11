from fastapi import HTTPException


class InvalidEmailException(HTTPException):
    def __init__(self, email: str):
        self.status_code = 400
        self.detail = f"Invalid email: {email}."
