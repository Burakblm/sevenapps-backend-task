import google.generativeai as genai
from sqlalchemy.orm import Session

from app import models
from app.core.config import settings

genai.configure(api_key=settings.GOOGLE_GENERATIVE_AI_API)

class ChatService:
    def __init__(self, db: Session):
        """
        Initializes the ChatService with a database session.

        Args:
            db (Session): SQLAlchemy database session.
        """
        self.db = db

    def get_pdf_record(self, pdf_id: str):
        """
        Fetches a PDF record from the database by its document ID.

        Args:
            pdf_id (str): The ID of the PDF document.

        Returns:
            Pdf | None: The PDF record if found, otherwise None.
        """
        pdf_record = (
            self.db.query(models.Pdf).filter(models.Pdf.document_id == pdf_id).first()
        )
        if not pdf_record:
            return None
        return pdf_record

    def check_pdf_status(self, pdf_record):
        """
        Checks if the PDF has a "completed" status.

        Args:
            pdf_record (Pdf): The PDF record to check.

        Returns:
            bool: True if the PDF status is "completed", False otherwise.
        """
        return pdf_record.document_status == "completed"

    def extract_text_from_pdf(self, pdf_record):
        """
        Extracts the text content from a PDF record.

        Args:
            pdf_record (Pdf): The PDF record containing text data.

        Returns:
            str: The extracted text data from the PDF.
        """
        return pdf_record.text_data

    def generate_ai_response(self, pdf_text, pdf_record, user_message: str):
        """
        Sends a query to the AI model with PDF content, metadata, and user message.

        Args:
            pdf_text (str): The text content extracted from the PDF.
            pdf_record (Pdf): The PDF record from the database.
            user_message (str): The user's query/message.

        Returns:
            str: The AI response or an error message if generation fails.
        """
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")

            filename = pdf_record.filename
            page_count = len(pdf_record.text_data.split("\n"))

            prompt = f"""
            **PDF Metadata:**
            - Filename: {filename}
            - Page Count: {page_count}

            **PDF Content:**
            {pdf_text}

            **User Question:**
            {user_message}

            **Response:**
            """

            response = model.generate_content(prompt)
            return response.text

        except Exception as e:
            return f"An error occurred while generating the AI response: {str(e)}"
