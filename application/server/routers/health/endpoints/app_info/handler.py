from config import openapi_config
from fastapi import APIRouter

from common.utils import async_wrapper
from clients import parser_client
from dbs import mongo_adapter
from .schemas import Msg

router = APIRouter()


@router.post('/system-status/', response_model=Msg, status_code=200)
async def check_app_status() -> Msg:
    """
    Check app status.
    # Check Client
    # Check DB  # TODO: Not Implemented
    # Check application
    """

    await async_wrapper(parser_client.get_page)('https://www.google.com/')
    await mongo_adapter.get_db()
    return Msg(**{'msg': 'Ok'})


@router.post('/app-version/', response_model=Msg, status_code=200)
async def check_app_version() -> Msg:
    """
    Check app version.
    """
    return Msg(**{'msg': openapi_config.version})
