"""
Here you should do all needed actions. Standart configuration of docker container
will run your application with this file.
"""

import sentry_sdk
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from loguru import logger
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from config import application_config, mongodb_config, openapi_config, sentry_config
from dbs import mongo_adapter
from web.core.exceptions import (
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTPException,
    http_422_error_handler,
    http_error_handler,
)
from web.core.middleware import (
    add_process_time_header,
    logging_access_token,
    request_context_log_middleware,
    request_logging_middleware,
    server_check_middleware,
    set_server_is_working,
    set_server_is_not_working,
)
from web.routers import base_router as routers
from .utils import cancel_all_tasks

GRACEFULLY_SHUTDOWN_TIMEOUT = 30

logger.info('Starting application initialization...')


app = FastAPI(
    title=openapi_config.name,
    version=openapi_config.version,
    description=openapi_config.description,
    debug=application_config.is_debug,
)
app.add_exception_handler(HTTPException, http_error_handler)
app.add_exception_handler(HTTP_422_UNPROCESSABLE_ENTITY, http_422_error_handler)

app.middleware('http')(  # for func middleware
    logging_access_token
)  # didn't work like decorator if func not main module
app.middleware('http')(  # for func middleware
    add_process_time_header
)  # didn't work like decorator if func not main module
app.middleware('http')(  # for func middleware
    request_context_log_middleware
)  # didn't work like decorator if func not main module
app.middleware('http')(  # for func middleware
    request_logging_middleware
)  # didn't work like decorator if func not main module
app.middleware('http')(  # for func middleware
    server_check_middleware
)  # didn't work like decorator if func not main module


if sentry_config.dsn:
    sentry_sdk.init(dsn=sentry_config.dsn)
    app.add_middleware(SentryAsgiMiddleware)

app.include_router(routers)
logger.success('Successfully initialized!')


@app.on_event('startup')
async def startup():
    await mongo_adapter.init(mongodb_config)
    await mongo_adapter.auth_mongo()
    set_server_is_working()


@app.on_event('shutdown')
async def shutdown():
    set_server_is_not_working()
    await mongo_adapter.close_connections()
    await cancel_all_tasks(timeout=GRACEFULLY_SHUTDOWN_TIMEOUT)


@app.get('/')
async def redirect_to_docs():
    return RedirectResponse('/docs')
