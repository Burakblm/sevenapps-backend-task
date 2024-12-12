import logging
import os

import pdfplumber

logger = logging.getLogger(__name__)


def get_page_count_and_text(pdf_file_path: str):
    try:
        text_data = ""
        with pdfplumber.open(pdf_file_path) as pdf:
            page_count = len(pdf.pages)
            for page in pdf.pages:
                text_data += page.extract_text() or ""
        logger.debug(f"Extracted {page_count} pages from {pdf_file_path}.")
        return page_count, text_data
    except Exception as e:
        logger.error(f"Error processing PDF {pdf_file_path}: {e}")
        return 0, ""


def delete_pdf_file(pdf_file_path: str):
    try:
        if os.path.exists(pdf_file_path):
            os.remove(pdf_file_path)
            logger.info(f"Deleted file: {pdf_file_path}")
        else:
            logger.warning(f"File not found: {pdf_file_path}")
    except Exception as e:
        logger.error(f"Error deleting file {pdf_file_path}: {e}")
