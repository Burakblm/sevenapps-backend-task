from pydantic import BaseModel


class PdfOut(BaseModel):
    pdf_id: str

