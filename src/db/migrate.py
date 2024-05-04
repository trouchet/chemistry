import asyncio
from sqlalchemy.ext.asyncio import create_async_engine

from src.api.setup.logging import logger
from src.db.schemas import Base
from src.db.engine import async_database_engine

async def migrate_tables() -> None:
    logger.info("Starting to migrate")

    async with async_database_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    logger.info("Done migrating")


if __name__ == "__main__":
    asyncio.run(migrate_tables())
