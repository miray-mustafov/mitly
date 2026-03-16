from fastapi import APIRouter
from .routes import urls

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(urls.router)
