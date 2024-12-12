import logging
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas
from app.core.db import get_db
from app.services.pdf_service import PdfService
from app.utils import validate_file_size, validate_file_type

router = APIRouter(prefix="/pdf", tags=["Pdf"])

logger = logging.getLogger(__name__)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PdfOut)
async def upload_pdf(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Receives a PDF file, uploads it to Google Cloud Storage, and adds metadata (document_id and filename) to the database.
    Additionally, it checks the file size and validates if the file is in PDF format.
    """
    logger.info("Received a request to upload a PDF file.")

    validate_file_size(file.size)
    validate_file_type(file.content_type)

    pdf_service = PdfService(db)

    try:
        logger.info(f"Processing file upload for: {file.filename}")
        pdf_data = await pdf_service.upload_pdf(file)
        logger.info(f"File successfully uploaded and metadata stored: {pdf_data.document_id}")
    except Exception as e:
        logger.error(f"An error occurred while processing the PDF file: {file.filename}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing the PDF: {str(e)}",
        )

    return {"pdf_id": pdf_data.document_id}
