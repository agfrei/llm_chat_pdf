from fastapi import APIRouter

from src.app.api.endpoints.file import router as file_router

api_router = APIRouter()
api_router.include_router(file_router, prefix="/file", tags=["file"])
