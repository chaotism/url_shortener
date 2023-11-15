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


class CustomSignalHandlerServer(uvicorn.Server):
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
        counter = 0
        should_exit = await self.on_tick(counter)
        while not should_exit:
            counter += 1
            counter = counter % 864000
            await asyncio.sleep(0.1)
            should_exit = await self.on_tick(counter)

        await self.close_server_active_connection()

    # def handle_exit(self, sig: int, frame: Optional[FrameType]) -> None:
    #     set_server_is_not_working(self.config.app)
    #     asyncio.ensure_future(self.wait_server_active_connection())
    #     # asyncio.ensure_future(cancel_all_tasks(timeout=GRACEFULLY_SHUTDOWN_TIMEOUT))
    #     with threading.RLock():
    #         timer = threading.Timer(
    #             self.shutdown_delay,
    #             super().handle_exit,
    #             kwargs=dict(sig=sig, frame=frame),
    #         )
    #         timer.start()


if __name__ == '__main__':
    config = uvicorn.Config(
        app=app,
        host=application_config.host,
        port=application_config.port,
        loop='asyncio',
    )
    server = CustomSignalHandlerServer(
        config=config,
    )
    server.run()
