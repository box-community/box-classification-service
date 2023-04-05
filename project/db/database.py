"""Database connection and base class."""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from app.config import Settings


def create_db_engine(settings: Settings):
    """Create the database engine."""
    return create_engine(
        settings.SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
    )


Base = declarative_base()
