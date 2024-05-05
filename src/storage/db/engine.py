from sqlalchemy.ext.asyncio import create_async_engine
from src.setup.config import settings

# Cria uma instância de engine do banco de dados
async def create_async_database_engine(
    uri: str = settings.POSTGRES_URI,
    show_echo: bool = settings.POSTGRES_ECHO,
):
    """
    Creates an asynchronous engine for the database.

    This function is asynchronous and should be awaited to get the engine object.

    Returns:
        sqlalchemy.ext.asyncio.AsyncEngine: The asynchronous engine for the database.
    """
    return await create_async_engine(uri, echo=show_echo, future=True)

