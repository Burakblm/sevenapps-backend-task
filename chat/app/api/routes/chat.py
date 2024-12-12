from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging

from app import schemas
from app.core.db import get_db
from app.services.chat_service import ChatService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/{pdf_id}", response_model=schemas.ChatResponse)
async def chat_with_pdf(
    pdf_id: str, message: schemas.Message, db: Session = Depends(get_db)
):
    """
    Responds to the user's message with the PDF's metadata and content.
    
    Args:
        pdf_id (str): The ID of the PDF document.
        message (schemas.Message): The user's message for context.
        db (Session): The database session dependency.
    
    Returns:
        dict: AI-generated response to the user's query based on PDF content.
    """
    try:
        chat_service = ChatService(db)

        pdf_record = chat_service.get_pdf_record(pdf_id)
        if not pdf_record:
            logger.warning(f"PDF not found: {pdf_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="PDF not found"
            )

        if not chat_service.check_pdf_status(pdf_record):
            logger.info(f"PDF {pdf_id} is not ready yet.")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="PDF is not ready yet. Please try again later.",
            )

        pdf_text = chat_service.extract_text_from_pdf(pdf_record)
        if not pdf_text:
            logger.warning(f"No text found for PDF {pdf_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No text data found for this PDF",
            )

        response = chat_service.generate_ai_response(
            pdf_text, pdf_record, message.message
        )

        return {"response": response}

    except HTTPException as http_error:
        logger.error(f"HTTP error occurred: {str(http_error.detail)}")
        raise http_error

    except Exception as e:
        logger.error(f"Unexpected error occurred: {str(e)}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
