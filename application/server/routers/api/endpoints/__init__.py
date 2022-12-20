from fastapi import APIRouter

from .shorter import url_shorter_router

api_router = APIRouter(prefix='/v1')

api_router.include_router(
    url_shorter_router, prefix='/urls_shorter', tags=['urls_shorter']
)
