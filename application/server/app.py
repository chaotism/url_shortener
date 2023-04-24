"""
Here you should do all needed actions. Standart configuration of docker container
will run your application with this file.
"""
import sentry_sdk
import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from loguru import logger
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from clients import parser_client
from common.utils import async_wrapper
from config import (
    application_config,
    mongodb_config,
    parser_config,
    openapi_config,
    sentry_config,
)
from dbs import mongo_adapter
from server.core.exceptions import (
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTPException,
    http_422_error_handler,
    http_error_handler,
)
from server.core.middleware import add_process_time_header, logging_access_token
from server.routers import base_router as routers

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
if sentry_config.dsn:
    sentry_sdk.init(dsn=sentry_config.dsn)
    app.add_middleware(SentryAsgiMiddleware)

app.include_router(routers)
logger.success('Successfully initialized!')


@app.on_event('startup')
async def startup():
    await mongo_adapter.init(mongodb_config)
    await mongo_adapter.auth_mongo()
    await async_wrapper(parser_client.init)(parser_config)


@app.on_event('shutdown')
async def shutdown():
    await mongo_adapter.close_connections()
    await async_wrapper(parser_client.close_client)()


@app.get('/')
async def redirect_to_docs():
    return RedirectResponse('/docs')


if __name__ == '__main__':
    uvicorn.run(
        'server.app:app',
        host=application_config.host,
        port=application_config.port,
        reload=True,
    )
