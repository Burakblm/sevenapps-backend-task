from io import BytesIO

import pytest
from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import app

@pytest.fixture
def client():
    """
    Creates a TestClient instance for testing the FastAPI application.
    """
    return TestClient(app)

def test_upload_pdf_file_too_large(client):
    """
    Tests that uploading a PDF file exceeding the size limit results in a 400 Bad Request response.

    Simulates a file larger than 10 MB and verifies that the API rejects it with the correct status code.
    """
    large_file = BytesIO(b"A" * (11 * 1024 * 1024))
    large_file.name = "large_file.pdf"

    response = client.post(
        f"{settings.API_V1_STR}/pdf",
        files={"file": ("large_file.pdf", large_file, "application/pdf")},
    )

    assert response.status_code == 400

def test_upload_valid_pdf(client):
    """
    Tests that a valid PDF file is successfully uploaded and processed.

    Simulates a valid PDF file and verifies that the response contains a `pdf_id` field with the correct data type.
    """
    valid_pdf = BytesIO(b"%PDF-1.4\n%\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1\n...")
    valid_pdf.name = "valid_file.pdf"

    response = client.post(
        f"{settings.API_V1_STR}/pdf",
        files={"file": ("valid_file.pdf", valid_pdf, "application/pdf")},
    )

    assert response.status_code == 201
    response_data = response.json()
    assert "pdf_id" in response_data
    assert isinstance(response_data["pdf_id"], str)

def test_upload_non_pdf_file(client):
    """
    Tests that uploading a non-PDF file results in a 400 Bad Request response.

    Simulates a text file upload and verifies that the API rejects it with an appropriate error message.
    """
    non_pdf_file = BytesIO(b"This is a text file, not a PDF.")
    non_pdf_file.name = "invalid_file.txt"

    response = client.post(
        f"{settings.API_V1_STR}/pdf",
        files={"file": ("invalid_file.txt", non_pdf_file, "text/plain")},
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Invalid file format. Only PDF files are accepted."
    }

def test_upload_valid_pdf_and_check_response_model(client):
    """
    Tests that a valid PDF upload returns the correct response model.

    Simulates a valid PDF file and checks the structure and content of the response, including the presence and type of `pdf_id`.
    """
    valid_pdf = BytesIO(b"%PDF-1.4\n%\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1\n...")
    valid_pdf.name = "valid_file.pdf"

    response = client.post(
        f"{settings.API_V1_STR}/pdf",
        files={"file": ("valid_file.pdf", valid_pdf, "application/pdf")},
    )

    assert response.status_code == 201

    response_data = response.json()

    assert "pdf_id" in response_data
    assert isinstance(response_data["pdf_id"], str)
    assert len(response_data["pdf_id"]) > 0
