"""
Here you should do all needed actions. Standart configuration of docker container
will run your application with this file.
"""
import threading
from types import FrameType
from typing import Optional

import uvicorn

from config import application_config
from web.app import app, set_server_is_not_working, GRACEFULLY_SHUTDOWN_TIMEOUT


class CustomSignalHandlerServer(uvicorn.Server):
    shutdown_delay = GRACEFULLY_SHUTDOWN_TIMEOUT

    def handle_exit(self, sig: int, frame: Optional[FrameType]) -> None:
        set_server_is_not_working()
        with threading.RLock():
            timer = threading.Timer(
                self.shutdown_delay,
                super().handle_exit,
                kwargs=dict(sig=sig, frame=frame),
            )
            timer.start()


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
