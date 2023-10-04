from fastapi import FastAPI

from src.app.api.api import api_router

app = FastAPI()

app.include_router(api_router)
