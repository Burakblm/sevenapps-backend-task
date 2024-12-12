import uuid

from sqlalchemy import TIMESTAMP, Column, Integer, String
from sqlalchemy.sql.expression import text

from app.core.db import Base


class Pdf(Base):
    __tablename__ = "pdf"

    id = Column(Integer, primary_key=True, nullable=False)
    document_id = Column(
        String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4())
    )
    filename = Column(String, nullable=False)
    text_data = Column(String, nullable=True)
    document_status = Column(String, nullable=False, default="pending")
    page_count = Column(Integer, nullable=True)  # Sayfa sayısı
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
