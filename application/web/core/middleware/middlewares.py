'''API Middlewares'''
import time
from uuid import uuid4

from fastapi import Request
from loguru import logger
from starlette.exceptions import HTTPException

from .utils import (
    is_server_working,
    get_request_id,
    set_request_id,
    get_correlation_id,
    set_correlation_id,
)


async def server_check_middleware(request: Request, call_next):
    if not is_server_working():
        raise HTTPException(status_code=503)
    response = await call_next(request)
    return response


async def request_context_log_middleware(request: Request, call_next):
    correlation_id_token = set_correlation_id(
        request.headers.get('X-Correlation-ID', str(uuid4()))
    )
    request_id_token = set_request_id(request.headers.get('X-Request-ID', str(uuid4())))
    response = await call_next(request)
    response.headers['X-Correlation-ID'] = get_correlation_id()
    response.headers['X-Request-ID'] = get_request_id()

    correlation_id_token.var.reset(correlation_id_token)
    request_id_token.var.reset(request_id_token)
    return response


async def request_logging_middleware(request: Request, call_next):
    logger.info('request:  %s %s', request.method, request.url.path)
    response = await call_next(request)
    logger.info(
        'response %s %s %s', request.method, request.url.path, response.status_code
    )
    return response


async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers['X-Process-Time'] = str(process_time)
    return response


async def logging_access_token(request: Request, call_next):
    method = request.method
    receive = request.receive
    access_token = request.headers.get('Auth-Token', '')
    remote_ip = request.headers.get('X-Real-IP', '')
    logger.info(
        '%s to %s for IP %s with token %s', method, receive, remote_ip, access_token
    )
    response = await call_next(request)
    return response
