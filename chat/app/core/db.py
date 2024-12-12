import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

logger = logging.getLogger(__name__)

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)

logger.debug(f"Database URI: {settings.SQLALCHEMY_DATABASE_URI}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def create_tables():
    """
    Creates all database tables by reflecting the base models defined.
    """
    try:
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Tables created successfully.")
    except Exception as e:
        logger.error("Error occurred while creating tables", exc_info=True)
        raise Exception("Failed to create tables") from e


def get_db():
    """
    Provides a database session for use in the application. Ensures proper cleanup of the session.
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error("An error occurred while handling the database session.", exc_info=True)
        raise e
    finally:
        db.close()
        logger.debug("Database session closed.")
