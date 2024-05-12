from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse


from ..dependencies.users import CurrentUserDependency, get_current_active_superuser
from ..dependencies.session import DatabaseSessionDependency
from ..dependencies.auth import PasswordFormDependency

from ... import settings
from ..utils.security import (
    get_password_hash,
    create_access_token,
)

from ..services.users import (
    authenticate,
    get_user_by_email,
)

from backend.app.exceptions import (
    WrongCredentialsException,
    InactiveUserException,
    InvalidTokenException,
    InexistentUserByEmailException,
)

from ..utils.email import (
    generate_password_reset_token,
    generate_reset_password_email,
    send_email,
    verify_password_reset_token,
)

from ...models.email import Message
from ...models.token import Token
from ...models.users import NewPassword, UserPublic


router = APIRouter()


@router.post("/login/access-token")
def login_access_token(
    session: DatabaseSessionDependency, form_data: PasswordFormDependency
) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = authenticate(
        session=session, email=form_data.username, password=form_data.password
    )

    if not user:
        raise WrongCredentialsException()

    elif not user.is_active:
        raise InactiveUserException()

    expire_timedelta_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    access_token_expires = timedelta(minutes=expire_timedelta_minutes)
    access_token = create_access_token(user.id, expires_delta=access_token_expires)

    return Token(access_token=access_token)


@router.post("/login/test-token", response_model=UserPublic)
def test_token(current_user: CurrentUserDependency) -> Any:
    """
    Test access token
    """
    return current_user


@router.post("/password-recovery/{email}")
def recover_password(email: str, session: DatabaseSessionDependency) -> Message:
    """
    Password Recovery
    """
    user = get_user_by_email(session=session, email=email)

    if not user:
        raise InexistentUserByEmailException()

    password_reset_token = generate_password_reset_token(email=email)
    email_data = generate_reset_password_email(
        email_to=user.email, email=email, token=password_reset_token
    )
    send_email(
        email_to=user.email,
        subject=email_data.subject,
        html_content=email_data.html_content,
    )
    return Message(message="Password recovery email sent")


@router.post("/reset-password/")
def reset_password(session: DatabaseSessionDependency, body: NewPassword) -> Message:
    """
    Reset password
    """
    email = verify_password_reset_token(token=body.token)
    if not email:
        raise InvalidTokenException()

    user = get_user_by_email(session=session, email=email)
    if not user:
        raise InexistentUserByEmailException()

    if not user.is_active:
        raise InactiveUserException()

    hashed_password = get_password_hash(password=body.new_password)
    user.hashed_password = hashed_password
    session.add(user)
    session.commit()

    return Message(message="Password updated successfully")


@router.post(
    "/password-recovery-html-content/{email}",
    dependencies=[Depends(get_current_active_superuser)],
    response_class=HTMLResponse,
)
def recover_password_html_content(
    email: str, session: DatabaseSessionDependency
) -> Any:
    """
    HTML Content for Password Recovery
    """
    user = get_user_by_email(session=session, email=email)

    if not user:
        raise InexistentUserByEmailException()

    password_reset_token = generate_password_reset_token(email=email)
    email_data = generate_reset_password_email(
        email_to=user.email, email=email, token=password_reset_token
    )

    return HTMLResponse(
        content=email_data.html_content, headers={"subject:": email_data.subject}
    )
