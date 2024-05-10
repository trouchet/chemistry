from fastapi import APIRouter, Depends
from pydantic.networks import EmailStr

from backend.app.api.dependencies.users import get_current_active_superuser
from backend.app.api.utils.email import (
    generate_test_email, 
    send_email
)
from backend.app.db.models.misc import Message 

router = APIRouter()


@router.post(
    "/test-email/",
    dependencies=[Depends(get_current_active_superuser)],
    status_code=201,
)
def test_email(email_to: EmailStr) -> Message:
    """
    Test emails.
    """
    email_data = generate_test_email(email_to=email_to)
    send_email(
        email_to=email_to,
        subject=email_data.subject,
        html_content=email_data.html_content,
    )
    return Message(message="Test email sent")