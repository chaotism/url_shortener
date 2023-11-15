'''API Middlewares utils'''

from fastapi import FastAPI
from contextvars import ContextVar, copy_context, Token

from pydantic import BaseModel


SERVER_STATE_KEY = 'server_state'

CORRELATION_ID_CTX_KEY = 'correlation_id'
REQUEST_ID_CTX_KEY = 'request_id'


_ctx = copy_context()


_correlation_id_ctx_var: ContextVar[str] = ContextVar(
    CORRELATION_ID_CTX_KEY, default='undefined'
)
_request_id_ctx_var: ContextVar[str] = ContextVar(
    REQUEST_ID_CTX_KEY, default='undefined'
)


class ServerStats(BaseModel):
    active_requests: int = 0
    running: bool = False

    def increase_request_count(self):
        self.active_requests += 1

    def decrease_request_count(self):
        self.active_requests -= 1

    def has_active_request(self) -> bool:
        return self.active_requests > 0

    def set_running(self):
        self.running = True

    def set_stopping(self):
        self.running = False

    def is_running(self) -> bool:
        return self.running


def is_server_working(application: FastAPI) -> bool:
    if not application.extra[SERVER_STATE_KEY]:
        raise KeyError(f'Cannot find {[SERVER_STATE_KEY]} server state key')
    return application.extra[SERVER_STATE_KEY].is_running()


def init_server_state(application: FastAPI):
    application.extra[SERVER_STATE_KEY] = ServerStats()


def set_server_is_working(application: FastAPI):
    application.extra[SERVER_STATE_KEY].set_running()


def set_server_is_not_working(application: FastAPI):
    application.extra[SERVER_STATE_KEY].set_stopping()


def increase_server_count_active_request(application: FastAPI):
    application.extra[SERVER_STATE_KEY].increase_request_count()


def decrease_server_count_active_request(application: FastAPI):
    application.extra[SERVER_STATE_KEY].decrease_request_count()


def has_server_active_request(application: FastAPI) -> bool:
    return application.extra[SERVER_STATE_KEY].has_active_request()


def get_correlation_id() -> str:
    return _correlation_id_ctx_var.get()


def set_correlation_id(correlation_id: str) -> Token[str]:
    return _request_id_ctx_var.set(correlation_id)


def get_request_id() -> str:
    return _request_id_ctx_var.get()


def set_request_id(request_id: str) -> Token[str]:
    return _request_id_ctx_var.set(request_id)
