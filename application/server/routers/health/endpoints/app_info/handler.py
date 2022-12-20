from typing import Any

from config import openapi_config
from fastapi import APIRouter

from .schemas import Msg

router = APIRouter()


@router.post('/system-status/', response_model=Msg, status_code=200)
def check_app_status() -> Any:
    """
    Check app status.
    # Check DB  # TODO: Not Implemented
    # Check application
    """
    return {'msg': 'Ok'}


@router.post('/app-version/', response_model=Msg, status_code=200)
def check_app_version() -> Any:
    """
    Check app version.
    """
    return {'msg': openapi_config.version}
