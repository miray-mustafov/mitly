from fastapi import APIRouter
from .routes import public

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(public.router, tags=["URLs"])
