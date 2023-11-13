'''API Middlewares utils'''

from contextvars import ContextVar, copy_context, Token

IS_SERVER_WORKING_CTX_KEY = 'is_working'
CORRELATION_ID_CTX_KEY = 'correlation_id'
REQUEST_ID_CTX_KEY = 'request_id'


_ctx = copy_context()

_is_server_working_ctx_var: ContextVar[bool] = ContextVar(
    IS_SERVER_WORKING_CTX_KEY, default=False
)
_correlation_id_ctx_var: ContextVar[str] = ContextVar(
    CORRELATION_ID_CTX_KEY, default='undefined'
)
_request_id_ctx_var: ContextVar[str] = ContextVar(
    REQUEST_ID_CTX_KEY, default='undefined'
)


def is_server_working() -> bool:
    return _ctx.run(_is_server_working_ctx_var.get)


def set_server_is_working() -> Token[bool]:
    return _ctx.run(_is_server_working_ctx_var.set, True)


def set_server_is_not_working() -> Token[bool]:
    return _ctx.run(_is_server_working_ctx_var.set, False)


def get_correlation_id() -> str:
    return _correlation_id_ctx_var.get()
    # return _ctx.run(_correlation_id_ctx_var.get)


def set_correlation_id(correlation_id: str) -> Token[str]:
    return _request_id_ctx_var.set(correlation_id)
    # return _ctx.run(_correlation_id_ctx_var.set, correlation_id)


def get_request_id() -> str:
    return _request_id_ctx_var.get()
    # return _ctx.run(_request_id_ctx_var.get)


def set_request_id(request_id: str) -> Token[str]:
    return _request_id_ctx_var.set(request_id)
    # return _ctx.run(_request_id_ctx_var.set, request_id)
