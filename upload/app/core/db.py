import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings

logger = logging.getLogger(__name__)

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def create_tables():
    """
    Creates the database tables based on the defined models.

    This function will create all tables if they don't already exist in the database.
    """
    try:
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Tables created successfully.")
    except Exception as e:
        logger.error("An error occurred while creating tables.", exc_info=True)
        raise

def get_db():
    """
    Provides a database session to be used in the application.

    This function ensures that a database session is created and properly closed
    after the request is handled. It also logs any exceptions that occur during
    the session lifecycle.

    Yields:
        db: The database session to be used for interactions with the database.
    """
    logger.info("Creating a new database session...")
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error("An error occurred during the database session.", exc_info=True)
        raise e
    finally:
        db.close()
        logger.info("Database session closed.")
