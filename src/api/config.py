from pydantic_settings import BaseSettings

from src.api.setup.logging import logging

logging.basicConfig(level=logging.INFO)
class Settings(BaseSettings):
    """App settings."""

    project_name: str = "API"
    debug: bool = False
    environment: str = "local"

    # Database
    database_url: str = ""


settings = Settings()