from fastapi import APIRouter

from app.api.routes import chat

api_router = APIRouter()

api_router.include_router(chat.router)
