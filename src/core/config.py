from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import Optional, Union, List
from os import environ
from dotenv import load_dotenv
from sqlalchemy.engine import URL
from asyncpg.pool import Pool
from aioredis import Redis
import toml

load_dotenv()

# Database information
POSTGRES_DB = environ.get("POSTGRES_DB")
POSTGRES_USER = environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = environ.get("POSTGRES_PASSWORD")
POSTGRES_HOST = environ.get("POSTGRES_HOST", "localhost")
POSTGRES_PORT = environ.get("POSTGRES_PORT", 5432)

DATABASE_URL = str(URL.create(
    drivername="postgresql",
    username=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    database=POSTGRES_DB,
    port=POSTGRES_PORT
))

# Environment information: development, testing, production
ENVIRONMENT = environ.get("ENVIRONMENT", 'development')

# JWT information: secret key, algorithm, and expiration time
SECRET_KEY = environ.get("SECRET_KEY")
JWT_ALGORITHM = environ.get("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 60)

with open("pyproject.toml", "r") as f:
    config = toml.load(f)


# Settings class
class Settings(BaseSettings):
    """App settings."""

    project_name: str = config["tool"]["poetry"]["name"]
    debug: bool = False
    environment: str = ENVIRONMENT

    # Database
    DATABASE_URL: str = DATABASE_URL
    
    # JWT
    SECRET_KEY: str = SECRET_KEY
    JWT_ALGORITHM: str = JWT_ALGORITHM

    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    def create_app_redis(self):
        self.REDIS = Redis.from_url(self.REDIS_URL, max_connections=10, decode_responses=True)

    class Config:
        case_sensitive = True

settings = Settings()

