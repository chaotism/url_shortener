from fastapi import APIRouter, Depends

from .api.endpoints import api_router
from .health.endpoints import health_router
from ..core.security import verify_auth_token

base_router = APIRouter()

base_router.include_router(
    api_router,
    prefix='/api',
    dependencies=[
        Depends(verify_auth_token),
    ],
)
base_router.include_router(health_router, prefix='/health')
