import logging

from backend.app.db.base import engine, init_db
from sqlmodel import Session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    logger.info("Creating initial data")
    
    with Session(engine) as session:
        init_db(session)
    
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
