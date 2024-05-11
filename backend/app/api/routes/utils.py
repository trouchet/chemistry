from fastapi import APIRouter
from pydantic.networks import EmailStr

from ..dependencies.users import SuperUserDependency
from ..utils.email import generate_test_email, send_email
from ...models.email import Message

router = APIRouter()


@router.post(
    "/test-email/",
    dependencies=[SuperUserDependency],
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
