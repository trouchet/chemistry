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

# Postgres settings
POSTGRES_ENGINE = "postgresql+asyncpg"

POSTGRES_DB = environ.get("POSTGRES_DB", "postgres")
POSTGRES_HOST = environ.get("POSTGRES_HOST", "localhost")
POSTGRES_PORT = environ.get("POSTGRES_PORT", 5432)
POSTGRES_USER = environ.get("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = environ.get("POSTGRES_PASSWORD", "postgres")

POSTGRES_DB_TEST = environ.get("POSTGRES_DB_TEST", "postgres")
POSTGRES_HOST_TEST = environ.get("POSTGRES_HOST_TEST", "localhost")
POSTGRES_PORT_TEST = environ.get("POSTGRES_PORT_TEST", 5435)
POSTGRES_USER_TEST = environ.get("POSTGRES_USER_TEST", "postgres")
POSTGRES_PASSWORD_TEST = environ.get("POSTGRES_PASSWORD_TEST", "postgres")

POSTGRES_ECHO = environ.get("POSTGRES_ECHO", "false")
POSTGRES_POOL_SIZE = environ.get("POSTGRES_POOL_SIZE", 10)

SECRET_KEY = environ.get("SECRET_KEY", "abc12345")
JWT_ALGORITHM = environ.get("JWT_ALGORITHM", "HS256")

class PostgresSettings:
    def __init__(
            self, engine:str, db: str, host: str, port: Union[int, str], 
            user: str, password: str, echo: bool = False, pool_size: int = 10
        ):
        self.engine = engine
        self.db = db
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.echo = echo
        self.pool_size = pool_size

    def __str__(self):
        route=f"{self.host}:{self.port}/{self.db}"
        credentials=f"{self.user}:{self.password}"
        return f"{self.engine}://{credentials}@{route}"

    def __repr__(self):
        route=f"{self.host}:{self.port}/{self.db}"
        credentials=f"{self.user}:{self.password}"
        return f"{self.engine}://{credentials}@{route}"

# Database settings
application_db_settings = PostgresSettings(
    POSTGRES_ENGINE, POSTGRES_DB, 
    POSTGRES_HOST,  POSTGRES_PORT, POSTGRES_USER, POSTGRES_PASSWORD,
    POSTGRES_ECHO, POSTGRES_POOL_SIZE
)
application_db_uri = str(application_db_settings)

test_db_settings = PostgresSettings(
    POSTGRES_ENGINE, POSTGRES_DB_TEST, 
    POSTGRES_HOST_TEST, POSTGRES_PORT_TEST, POSTGRES_USER, POSTGRES_PASSWORD,
    POSTGRES_ECHO, POSTGRES_POOL_SIZE
)
test_db_uri = str(test_db_settings)

class JWTSettings:
    def __init__(self, secret_key: str, algorithm: str, access_token_expire_minutes: int):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes

    def __str__(self):
        content=f"{self.secret_key}, {self.algorithm}, {self.access_token_expire_minutes}"
        return f"JWTSettings({content})"

    def __repr__(self):
        content=f"{self.secret_key}, {self.algorithm}, {self.access_token_expire_minutes}"
        return f"JWTSettings({content})"

# JWT settings
jwt_settings = JWTSettings(SECRET_KEY, JWT_ALGORITHM, 60 * 24 * 7)

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

    # Postgres settings
    POSTGRES_APPLICATION_SETTINGS: PostgresSettings = Field(application_db_settings)
    POSTGRES_TEST_SETTINGS: PostgresSettings = Field(test_db_settings)
    
    ASYNC_POSTGRES_URI: str = Field(application_db_uri)
    ASYNC_POSTGRES_URI_TEST: str = Field(test_db_uri)

    # JWT
    JWT_SETTINGS: JWTSettings = Field(jwt_settings)

    class Config(ConfigDict):
        case_sensitive = True
        env_file = ".env"


settings = Settings()
