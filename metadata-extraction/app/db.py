import logging
from config import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)

try:
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
    logger.info("Database engine created successfully.")
except Exception as e:
    logger.error(f"Error creating database engine: {e}")
    raise

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def create_tables():
    """
    Creates tables in the database based on the models defined.
    """
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Tables created successfully.")
    except Exception as e:
        logger.error(f"Error creating tables: {e}", exc_info=True)
        raise

def get_db():
    """
    Provides a database session and ensures it is properly closed after use.
    """
    db = SessionLocal()
    try:
        logger.debug("Database session opened.")
        yield db
    except Exception as e:
        logger.error(f"Database session error: {e}", exc_info=True)
        raise
    finally:
        db.close()
        logger.debug("Database session closed.")
