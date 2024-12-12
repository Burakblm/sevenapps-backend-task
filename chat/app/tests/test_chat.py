from unittest.mock import MagicMock
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models import Pdf
from app.services.chat_service import ChatService

client = TestClient(app)

@pytest.fixture
def mock_db():
    """
    Mocks the database session for testing purposes.
    """
    return MagicMock()

@pytest.fixture
def mock_chat_service(mock_db):
    """
    Mocks the ChatService for testing, associating it with a mocked database session.
    """
    chat_service = MagicMock(spec=ChatService)
    chat_service.db = mock_db
    return chat_service

def test_chat_with_pdf_success(mock_chat_service, mocker):
    """
    Tests that the chat API returns a successful response when interacting with a PDF.
    The mock responses simulate the expected behavior for extracting text and generating AI responses.
    """
    pdf_record = Pdf(
        document_id="123",
        document_status="completed",
        text_data="This is a sample PDF text",
        filename="sample.pdf",
    )

    mock_chat_service.get_pdf_record.return_value = pdf_record
    mock_chat_service.check_pdf_status.return_value = True
    mock_chat_service.extract_text_from_pdf.return_value = pdf_record.text_data
    mock_chat_service.generate_ai_response.return_value = "This is an AI-generated response."

    mocker.patch("app.api.routes.chat.ChatService", return_value=mock_chat_service)

    payload = {"message": "What is this PDF about?"}

    response = client.post("/v1/chat/123", json=payload)

    assert response.status_code == 200
    assert response.json() == {"response": "This is an AI-generated response."}
