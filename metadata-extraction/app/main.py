import logging
import logging.config
import time
from pathlib import Path

from config import settings
from db import get_db
from logging_config import setup_logging
from models import Pdf
from services.gcs_handler import download_pdf_from_gcs
from services.kafka_consumer import create_kafka_consumer
from services.pdf_handler import delete_pdf_file, get_page_count_and_text
from sqlalchemy.orm import Session

BASE_DIR = Path(__file__).parent
logging_config = setup_logging(BASE_DIR)
logging.config.dictConfig(logging_config)


logger = logging.getLogger(__name__)


def extract_metadata_and_update_status(
    document_id: str, pdf_file_path: str, db: Session
):
    try:
        page_count, text_data = get_page_count_and_text(pdf_file_path)

        pdf_record = db.query(Pdf).filter(Pdf.document_id == document_id).first()
        if pdf_record:
            pdf_record.page_count = page_count
            pdf_record.document_status = "completed"
            pdf_record.text_data = text_data
            db.commit()
            db.refresh(pdf_record)
            logger.info(f"Updated metadata for document ID {document_id}.")
        else:
            logger.warning(f"No record found for document ID {document_id}.")
        delete_pdf_file(pdf_file_path)
    except Exception as e:
        logger.error(f"Error updating status for {document_id}: {e}")
        raise


def consume_messages():
    consumer = create_kafka_consumer()
    while True:
        try:
            for message in consumer:
                document_id = message.value["document_id"]
                logger.info(f"Processing document ID: {document_id}")

                db = next(get_db())
                destination_file = f"{document_id}.pdf"
                download_pdf_from_gcs(
                    settings.BUCKET_NAME, document_id, destination_file
                )
                extract_metadata_and_update_status(document_id, destination_file, db)
        except Exception as e:
            logger.error(f"Error consuming messages: {e}")
            time.sleep(5)


if __name__ == "__main__":
    consume_messages()
