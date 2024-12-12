import logging
import logging.config
from pathlib import Path

from fastapi import FastAPI

from app.api.main import api_router
from app.core.config import settings
from app.core.db import create_tables
from app.core.logging_config import setup_logging

BASE_DIR = Path(__file__).parent
logging_config = setup_logging(BASE_DIR)
logging.config.dictConfig(logging_config)

logger = logging.getLogger(__name__)

try:
    logger.info("Creating database tables...")
    create_tables()
    logger.info("Database tables created successfully.")
except Exception as e:
    logger.error(f"Failed to create database tables: {str(e)}", exc_info=True)


logger.info("Initializing FastAPI application...")
app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.include_router(api_router, prefix=settings.API_V1_STR)

logger.info("Application startup completed successfully.")


@app.on_event("startup")
async def startup_event():
    logger.info("Application is starting up...")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application is shutting down...")
