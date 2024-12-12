import os
import uuid
from fastapi import HTTPException, status
from google.cloud import storage
from sqlalchemy.orm import Session

from app import models
from app.core.config import settings
from app.core.db import get_db
from app.core.kafka import CustomKafkaProducer

project_dir = os.path.dirname(os.path.abspath(__file__))

credentials_path = os.path.join(project_dir, 'credentials.json')

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

class PdfService:
    def __init__(self, db: Session):
        """
        Initializes the PdfService with the necessary dependencies:
        - Database session
        - Google Cloud Storage client
        - Kafka producer
        """
        self.db = db
        self.storage_client = storage.Client()
        self.bucket_name = settings.BUCKET_NAME
        self.kafka_producer = CustomKafkaProducer()

    async def upload_pdf(self, file) -> models.Pdf:
        """
        Uploads a PDF file to Google Cloud Storage and stores its metadata in the database.
        Also sends a message with the document ID to Kafka.

        Args:
            file: The PDF file to be uploaded.

        Returns:
            models.Pdf: The saved PDF metadata with the document ID and filename.
        """
        unique_id = uuid.uuid4().hex

        try:
            blob_name = self.upload_pdf_to_gcs(file, unique_id)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to upload PDF to Google Cloud Storage: {str(e)}",
            )

        try:
            pdf_data = models.Pdf(document_id=unique_id, filename=file.filename)
            self.db.add(pdf_data)
            self.db.commit()
            self.db.refresh(pdf_data)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to save PDF metadata to the database: {str(e)}",
            )

        try:
            self.kafka_producer.send_to_kafka(pdf_data.document_id)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to send message to Kafka: {str(e)}",
            )

        return pdf_data

    def upload_pdf_to_gcs(self, file, unique_id: str) -> str:
        """
        Uploads a PDF file to Google Cloud Storage and returns the blob name.

        Args:
            file: The file to be uploaded.
            unique_id: A unique identifier for the file to form the blob name.

        Returns:
            str: The blob name for the uploaded PDF file in Google Cloud Storage.
        """
        try:
            bucket = self.storage_client.bucket(self.bucket_name)
            blob_name = f"pdf/{unique_id}.pdf"
            blob = bucket.blob(blob_name)
            blob.upload_from_file(file.file, content_type="application/pdf")
            return blob_name
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to upload PDF to Google Cloud Storage: {str(e)}",
            )
