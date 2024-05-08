import logging

from sqlalchemy import Engine
from sqlmodel import Session, select
from tenacity import (
    after_log, 
    before_log, 
    retry, 
    stop_after_attempt, 
    wait_fixed,
)

from backend.storage.db import session_manager
from backend import logger

max_tries_seconds = 60 * 5  # 5 minutes
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries_seconds),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init(db_engine: Engine) -> None:
    try:
        # Try to create session to check if DB is awake
        with Session(db_engine) as session:
            session.exec(select(1))
    except Exception as e:
        logger.error(e)
        raise e


def main() -> None:
    logger.info("Initializing service")
    init(session_manager.engine)
    logger.info("Service finished initializing")


if __name__ == "__main__":
    main()