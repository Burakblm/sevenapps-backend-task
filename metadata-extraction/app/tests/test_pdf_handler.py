import os
import pytest
import tempfile
from app.services.pdf_handler import get_page_count_and_text, delete_pdf_file
from unittest.mock import patch

@pytest.fixture
def sample_pdf():
    temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    with open(temp_pdf.name, "wb") as f:
        f.write(
            b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R >>\nendobj\n4 0 obj\n<< /Length 55 >>\nstream\nBT /F1 24 Tf 72 720 Td (Hello, PDF!) Tj ET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f \n0000000010 00000 n \n0000000056 00000 n \n0000000112 00000 n \n0000000178 00000 n \ntrailer\n<< /Size 5 /Root 1 0 R >>\nstartxref\n244\n%%EOF"
        )
    yield temp_pdf.name

    if os.path.exists(temp_pdf.name):
        os.remove(temp_pdf.name)


def test_get_page_count_and_text(sample_pdf):
    page_count, text_data = get_page_count_and_text(sample_pdf)

    assert page_count == 1, "Page count should be 1."
    assert "Hello, PDF!" in text_data, "Extracted text should contain 'Hello, PDF!'"

 
def test_delete_pdf_file(sample_pdf):
    assert os.path.exists(sample_pdf), "PDF file should exist before deletion."

    delete_pdf_file(sample_pdf)

    assert not os.path.exists(sample_pdf), "PDF file should be deleted."
