from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import (
    AnyUrl,
    BeforeValidator,
    HttpUrl,
    PostgresDsn,
    computed_field,
    model_validator,
)


from typing import Literal, Annotated,List, Any
from typing_extensions import Self

from warnings import warn
from dotenv import load_dotenv
from os import environ
import toml

def parse_cors(v: Any) -> List[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)

DEFAULT_PASSWORD = "changethis"
POSTGRES_DSN_SCHEME = "postgresql+psycopg"

# Project settings
with open("pyproject.toml", "r") as f:
    config = toml.load(f)

# Settings class
class Settings(BaseSettings):
    """App settings."""
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )

    VERSION: str = config["tool"]["poetry"]["version"]
    PROJECT_NAME: str = config["tool"]["poetry"]["name"]
    API_STR: str = "/api"

    ENVIRONMENT: Literal['local'] = "development"
    DOMAIN: str = "localhost"
    
    # 7 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 7 * 24 * 60

    @computed_field  # type: ignore[misc]
    @property
    def server_host(self) -> str:
        # Use HTTPS for anything other than local development
        protocol = "http" if self.ENVIRONMENT == "local" else "https" 
        return f"{protocol}://{self.DOMAIN}"

    SENTRY_DSN: HttpUrl | None = None
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str = ""

    # Postgres settings
    @computed_field  # type: ignore[misc]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return str(
            MultiHostUrl.build(
                scheme=POSTGRES_DSN_SCHEME,
                username=self.POSTGRES_USER,
                password=self.POSTGRES_PASSWORD,
                host=self.POSTGRES_HOST,
                port=self.POSTGRES_PORT,
                path=self.POSTGRES_DB,
            )
        )
    
    # JWT
    SECRET_KEY: str
    JWT_ALGORITHM: str

    # CORS
    BACKEND_CORS_ORIGINS: Annotated[
        List[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []

    # Email settings
    SMTP_TLS: bool = True
    SMTP_SSL: bool = False
    SMTP_PORT: int = 587
    SMTP_HOST: str | None = None
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    
    # TODO: update type to EmailStr when sqlmodel supports it
    EMAILS_FROM_EMAIL: str | None = None
    EMAILS_FROM_NAME: str | None = None

    @model_validator(mode="after")
    def _set_default_emails_from(self) -> Self:
        if not self.EMAILS_FROM_NAME:
            self.EMAILS_FROM_NAME = self.PROJECT_NAME
        return self
    
    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48

    @computed_field  # type: ignore[misc]
    @property
    def emails_enabled(self) -> bool:
        return bool(self.SMTP_HOST and self.EMAILS_FROM_EMAIL)

    # TODO: update type to EmailStr when sqlmodel supports it
    EMAIL_TEST_USER: str = "test@example.com"
    # TODO: update type to EmailStr when sqlmodel supports it
    FIRST_SUPERUSER: str
    FIRST_SUPERUSER_PASSWORD: str
    USERS_OPEN_REGISTRATION: bool = False

    def _check_default_secret(self, var_name: str, value: str | None) -> None:
        if value == DEFAULT_PASSWORD:
            message = (
                f'The value of {var_name} is "{DEFAULT_PASSWORD}", '
                "for security, please change it, at least for deployments."
            )
            if self.ENVIRONMENT == "local":
                warn(message, stacklevel=1)
            else:
                raise ValueError(message)

    @model_validator(mode="after")
    def _enforce_non_default_secrets(self) -> Self:
        self._check_default_secret(
            "SECRET_KEY", self.SECRET_KEY
        )
        self._check_default_secret(
            "POSTGRES_PASSWORD", self.POSTGRES_PASSWORD
        )
        self._check_default_secret(
            "FIRST_SUPERUSER_PASSWORD", self.FIRST_SUPERUSER_PASSWORD
        )

        return self

settings = Settings()
