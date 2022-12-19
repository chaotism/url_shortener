"""
Here you should do all needed actions. Standart configuration of docker container
will run your application with this file.
"""
import uvicorn
from config import application_config

if __name__ == '__main__':
    uvicorn.run(
        'server.app:app',
        host=application_config.host,
        port=application_config.port,
        reload=True,
    )
