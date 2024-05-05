from pydantic_settings import BaseSettings
from pydantic import Field, field_validator, ConfigDict
from sqlalchemy.engine import URL
from typing import Dict, Any, Union

from dotenv import load_dotenv
from os import environ
import toml

load_dotenv()

# Environment variables
APP_HOST = environ.get("APP_HOST", '0.0.0.0')
APP_PORT = environ.get("APP_PORT", 8000)

ENVIRONMENT = environ.get("ENVIRONMENT", "development")

POSTGRES_DB = environ.get("POSTGRES_DB", "postgres")
POSTGRES_HOST = environ.get("POSTGRES_HOST", "localhost")
POSTGRES_PORT = environ.get("POSTGRES_PORT", 5432)
POSTGRES_USER = environ.get("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = environ.get("POSTGRES_PASSWORD", "postgres")
POSTGRES_ECHO = environ.get("POSTGRES_ECHO", "false")
POSTGRES_POOL_SIZE = environ.get("POSTGRES_POOL_SIZE", 10)

SECRET_KEY = environ.get("SECRET_KEY", "abc12345")
JWT_ALGORITHM = environ.get("JWT_ALGORITHM", "HS256")

# Project settings
with open("pyproject.toml", "r") as f:
    config = toml.load(f)


# Settings class
class Settings(BaseSettings):
    """App settings."""

    VERSION: str = config["tool"]["poetry"]["version"]

    PROJECT_NAME: str = config["tool"]["poetry"]["name"]

    APP_HOST: str = Field(APP_HOST)
    APP_PORT: int = Field(APP_PORT)

    # Environment information: development, testing, production
    ENVIRONMENT: str = Field(ENVIRONMENT)

    POSTGRES_DB: str = Field(POSTGRES_DB)
    POSTGRES_HOST: str = Field(POSTGRES_HOST)
    POSTGRES_PORT: Union[int, str] = Field(POSTGRES_PORT)
    POSTGRES_USER: str = Field(POSTGRES_USER)
    POSTGRES_PASSWORD: str = Field(POSTGRES_PASSWORD)

    POSTGRES_ECHO: bool = Field(POSTGRES_ECHO)
    POSTGRES_POOL_SIZE: int = Field(POSTGRES_POOL_SIZE)
    ASYNC_POSTGRES_URI: Union[None, str] = None
    ASYNC_POSTGRES_URI_TEST: Union[None, str] = None

    # JWT
    SECRET_KEY: str = Field(SECRET_KEY)
    JWT_ALGORITHM: str = Field(JWT_ALGORITHM)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = (
        60 * 24 * 7
    )  # 60 minutes * 24 hours * 7 days = 7 days

    @field_validator("ASYNC_POSTGRES_URI")
    def assemble_db_connection(cls, v: Union[None, str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v

        data = values.data

        return str(
            URL.create(
                drivername="postgresql+asyncpg",
                username=data.get("POSTGRES_USER"),
                password=data.get("POSTGRES_PASSWORD"),
                host=data.get("POSTGRES_HOST"),
                database=data.get("POSTGRES_DB"),
                port=int(data.get("POSTGRES_PORT")),
            )
        )
    
    @field_validator("ASYNC_POSTGRES_URI_TEST")
    def assemble_test_db_connection(cls, v: Union[None, str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v

        data = values.data

        return str(
            URL.create(
                drivername="postgresql",
                username=data.get("POSTGRES_USER"),
                password=data.get("POSTGRES_PASSWORD"),
                host=data.get("POSTGRES_HOST"),
                database=data.get("POSTGRES_DB")+'_test',
                port=int(data.get("POSTGRES_PORT")),
            )
        )

    class Config(ConfigDict):
        case_sensitive = True
        env_file = ".env"


settings = Settings()
