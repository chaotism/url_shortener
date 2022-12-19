from fastapi import APIRouter

from .api.endpoints import api_router
from .health.endpoints import health_router

base_router = APIRouter()

base_router.include_router(api_router, prefix='/api')
base_router.include_router(health_router, prefix='/health')
