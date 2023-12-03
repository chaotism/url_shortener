"""
Here you should do all needed actions. Standart configuration of docker container
will run your application with this file.
"""
import asyncio
from time import monotonic

import uvicorn

from config import application_config
from web.app import app, GRACEFULLY_SHUTDOWN_TIMEOUT
from web.core.middleware import has_server_active_request, set_server_is_not_working


class CustomCloseConnectionHandlerServer(uvicorn.Server):
    shutdown_delay = GRACEFULLY_SHUTDOWN_TIMEOUT

    async def close_server_active_connection(self):
        set_server_is_not_working(self.config.app)
        await self.wait_server_active_connection()

    async def wait_server_active_connection(self):
        start_time = monotonic()
        while monotonic() < start_time + self.shutdown_delay:
            if not has_server_active_request(self.config.app):
                return
            await asyncio.sleep(1)

    async def main_loop(self) -> None:
        await super().main_loop()
        await self.close_server_active_connection()


if __name__ == '__main__':
    config = uvicorn.Config(
        app=app,
        host=application_config.host,
        port=application_config.port,
        loop='asyncio',
    )
    server = CustomCloseConnectionHandlerServer(
        config=config,
    )
    server.run()
