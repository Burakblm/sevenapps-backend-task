from io import BytesIO

import pytest
from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_upload_pdf_file_too_large(client):
    # 11MB'lık bir dosya oluşturuyoruz
    large_file = BytesIO(b"A" * (11 * 1024 * 1024))
    large_file.name = "large_file.pdf"

    response = client.post(
        f"{settings.API_V1_STR}/pdf",
        files={"file": ("large_file.pdf", large_file, "application/pdf")},
    )

    assert response.status_code == 400


def test_upload_valid_pdf(client):
    # Geçerli bir PDF dosyası simüle ediyoruz
    valid_pdf = BytesIO(b"%PDF-1.4\n%\\xD0\\xCF\\x11\\xE0\\xA1\\xB1\\x1A\\xE1\n...")
    valid_pdf.name = "valid_file.pdf"

    response = client.post(
        f"{settings.API_V1_STR}/pdf",
        files={"file": ("valid_file.pdf", valid_pdf, "application/pdf")},
    )

    assert response.status_code == 201
    response_data = response.json()
    assert "pdf_id" in response_data
    assert isinstance(
        response_data["pdf_id"], str
    )  # pdf_id'nin string türünde olduğunu kontrol et


def test_upload_non_pdf_file(client):
    # PDF olmayan bir dosya (örneğin .txt dosyası)
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
    # Geçerli bir PDF dosyası simüle ediyoruz
    valid_pdf = BytesIO(b"%PDF-1.4\n%\\xD0\\xCF\\x11\\xE0\\xA1\\xB1\\x1A\\xE1\n...")
    valid_pdf.name = "valid_file.pdf"

    response = client.post(
        f"{settings.API_V1_STR}/pdf",
        files={"file": ("valid_file.pdf", valid_pdf, "application/pdf")},
    )

    assert response.status_code == 201

    # Dönen JSON verisini kontrol et
    response_data = response.json()

    # pdf_id'nin mevcut olup olmadığını ve doğru türde olduğunu kontrol et
    assert "pdf_id" in response_data
    assert isinstance(
        response_data["pdf_id"], str
    )  # pdf_id'nin string türünde olduğunu kontrol et
    assert len(response_data["pdf_id"]) > 0  # pdf_id'nin boş olmadığını kontrol et
