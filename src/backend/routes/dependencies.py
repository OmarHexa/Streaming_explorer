# from pyspark.sql import SparkSession
from typing import Iterator
from sqlalchemy.orm import Session

from database.config import SessionLocal

# Dependency for getting a database session
# see the following link to more about dependencies with yield
# https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/


def get_db() -> Iterator[Session]:
    """Yields a SQL database session for the api to query with SQLAlchemy."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

