from fastapi import APIRouter

from src.app.api.endpoints import chat_router, document_router

api_router = APIRouter()
api_router.include_router(
    document_router, prefix="/document", tags=["document"]
)
api_router.include_router(chat_router, prefix="/chat", tags=["chat"])
