from fastapi import APIRouter

from .app_info import app_info_router

health_router = APIRouter()
health_router.include_router(app_info_router, prefix='/app_info', tags=['app info'])
