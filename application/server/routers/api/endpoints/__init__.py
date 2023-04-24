from fastapi import APIRouter

from .parser import product_parser_router
from .shorter import url_shorter_router

api_router = APIRouter(prefix='/v1')


api_router.include_router(
    product_parser_router,
    prefix='/product_info',
    tags=['product_info'],
)

api_router.include_router(
    url_shorter_router, prefix='/urls_shorter', tags=['urls_shorter']
)
