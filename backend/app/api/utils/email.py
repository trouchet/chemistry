from typing import Dict
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Union
import emails  # type: ignore
import logging

from jinja2 import Template
from jwt import decode, encode, PyJWTError

from backend.app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class EmailData:
    html_content: str
    subject: str


def render_email_template(*, template_name: str, context: Dict[str, Any]) -> str:
    template_root = (
        Path(__file__).parent / ".." / "email-templates" / template_name
    )

    template_str = template_root.read_text()
    html_content = Template(template_str).render(context)
    return html_content


def send_email(
    *,
    email_to: str,
    subject: str = "",
    html_content: str = "",
) -> None:
    assert settings.emails_enabled, "no provided configuration for email variables"
    message = emails.Message(
        subject=subject,
        html=html_content,
        mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
    )
    smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}
    if settings.SMTP_TLS:
        smtp_options["tls"] = True
    elif settings.SMTP_SSL:
        smtp_options["ssl"] = True
    if settings.SMTP_USER:
        smtp_options["user"] = settings.SMTP_USER
    if settings.SMTP_PASSWORD:
        smtp_options["password"] = settings.SMTP_PASSWORD

    response = message.send(to=email_to, smtp=smtp_options)
    logger.info(f"send email result: {response}")


def generate_test_email(email_to: str) -> EmailData:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Test email"

    metadata = {"project_name": settings.PROJECT_NAME, "email": email_to}

    html_content = render_email_template(
        template_name="test_email.html",
        context=metadata,
    )

    return EmailData(html_content=html_content, subject=subject)


def generate_reset_password_email(email_to: str, email: str, token: str) -> EmailData:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Password recovery for user {email}"
    link = f"{settings.server_host}/reset-password?token={token}"
    metadata = {
        "project_name": settings.PROJECT_NAME,
        "username": email,
        "email": email_to,
        "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
        "link": link,
    }
    html_content = render_email_template(
        template_name="reset_password.mjml",
        context=metadata,
    )
    return EmailData(html_content=html_content, subject=subject)


def generate_new_account_email(
    email_to: str, username: str, password: str
) -> EmailData:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - New account for user {username}"
    metadata = {
        "project_name": settings.PROJECT_NAME,
        "username": username,
        "password": password,
        "email": email_to,
        "link": settings.server_host,
    }

    html_content = render_email_template(
        template_name="new_account.mjml", context=metadata
    )
    return EmailData(html_content=html_content, subject=subject)


def generate_password_reset_token(email: str) -> str:
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.now()
    expires = now + delta
    exp = expires.timestamp()

    jwt_content = {"exp": exp, "nbf": now, "sub": email}

    encoded_jwt = encode(jwt_content, settings.SECRET_KEY, algorithm="HS256")
    return encoded_jwt


def verify_password_reset_token(token: str) -> Union[str, None]:
    try:
        decoded_token = decode(
            token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        return str(decoded_token["sub"])
    except PyJWTError:
        return None
