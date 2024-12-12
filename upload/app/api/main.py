from fastapi import APIRouter

from app.api.routes import pdf

api_router = APIRouter()

api_router.include_router(pdf.router)
