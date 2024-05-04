# get the environment variables
import databases
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from src.core.config import settings

# Cria uma instância de engine do banco de dados
async_database_engine = create_async_engine(
    settings.ASYNC_POSTGRES_URI,
    echo=settings.POSTGRES_ECHO,
    future=True,
    pool_size=max(5, settings.POSTGRES_POOL_SIZE),
)

# Create all tables stored in this metadata in the actual file.
Base = declarative_base()

# Initialize a database connection.
raw_database_connection = databases.Database(settings.ASYNC_POSTGRES_URI)

# Crie uma sessão para interagir com o banco de dados
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_database_engine,
    expire_on_commit=False,
    class_=AsyncSession,
)
