from pydantic_settings import BaseSettings
from pydantic import Field, PostgresDsn, field_validator
from sqlalchemy.engine import URL

from dotenv import load_dotenv
from typing import Dict, Any, Union
import toml

load_dotenv()

with open("pyproject.toml", "r") as f:
    config = toml.load(f)

# Settings class
class Settings(BaseSettings):
    """App settings."""
    VERSION: str = config["tool"]["poetry"]["version"]

    PROJECT_NAME: str = config["tool"]["poetry"]["name"]

    ENVIRONMENT = "development"
    APP_HOST: str = Field('0.0.0.0', env='APP_HOST')
    APP_PORT: int = Field(8000, env='APP_PORT')

    # Environment information: development, testing, production
    ENVIRONMENT: str = Field("development", env="ENVIRONMENT")
 
    POSTGRES_DB: str = Field("postgres", env="POSTGRES_DB")
    POSTGRES_HOST: str = Field("localhost", env="POSTGRES_HOST")
    POSTGRES_PORT: Union[int, str] = Field(5432, env="POSTGRES_PORT")
    POSTGRES_USER: str = Field("postgres", env="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field("postgres", env="POSTGRES_PASSWORD")

    POSTGRES_ECHO: bool = Field(False, env="POSTGRES_ECHO")
    POSTGRES_POOL_SIZE: int = Field(10, env="POSTGRES_POOL_SIZE")
    ASYNC_POSTGRES_URI: Union[None, str] = None
    
    # JWT
    SECRET_KEY: str = Field('12345', env="SECRET_KEY")
    JWT_ALGORITHM: str = Field('HS256', env="JWT_ALGORITHM")

    # 60 minutes * 24 hours * 7 days = 7 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    @field_validator("ASYNC_POSTGRES_URI")
    def assemble_db_connection(
        cls, v: Union[None, str], 
        values: Dict[str, Any]
    ) -> Any:
        if isinstance(v, str):
            return v
        data = values.data
        
        return str(URL.create(
            drivername="postgresql+asyncpg",
            username=data.get("POSTGRES_USER"),
            password=data.get("POSTGRES_PASSWORD"),
            host=data.get("POSTGRES_HOST"),
            database=data.get("POSTGRES_DB"),
            port=int(data.get("POSTGRES_PORT"))
        ))

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()



