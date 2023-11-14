'''API Middlewares utils'''

from fastapi import FastAPI
from contextvars import ContextVar, copy_context, Token

IS_SERVER_WORKING_EXTRA_KEY = 'is_server_working'

CORRELATION_ID_CTX_KEY = 'correlation_id'
REQUEST_ID_CTX_KEY = 'request_id'


_ctx = copy_context()


_correlation_id_ctx_var: ContextVar[str] = ContextVar(
    CORRELATION_ID_CTX_KEY, default='undefined'
)
_request_id_ctx_var: ContextVar[str] = ContextVar(
    REQUEST_ID_CTX_KEY, default='undefined'
)


def is_server_working(application: FastAPI) -> bool:
    if not application.extra[IS_SERVER_WORKING_EXTRA_KEY]:
        raise KeyError(f'Cannot find {[IS_SERVER_WORKING_EXTRA_KEY]} server state key')
    return application.extra[IS_SERVER_WORKING_EXTRA_KEY]


def set_server_is_working(application: FastAPI):
    application.extra[IS_SERVER_WORKING_EXTRA_KEY] = True


def set_server_is_not_working(application: FastAPI):
    application.extra[IS_SERVER_WORKING_EXTRA_KEY] = False


def get_correlation_id() -> str:
    return _correlation_id_ctx_var.get()


def set_correlation_id(correlation_id: str) -> Token[str]:
    return _request_id_ctx_var.set(correlation_id)


def get_request_id() -> str:
    return _request_id_ctx_var.get()


def set_request_id(request_id: str) -> Token[str]:
    return _request_id_ctx_var.set(request_id)
