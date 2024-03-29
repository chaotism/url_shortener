import asyncio

from fastapi import APIRouter

from config import openapi_config
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
    await asyncio.sleep(10)

    return Msg(**{'msg': 'Ok'})


@router.post('/app-version/', response_model=Msg, status_code=200)
async def check_app_version() -> Msg:
    """
    Check app version.
    """
    return Msg(**{'msg': openapi_config.version})
