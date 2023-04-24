# The project structure

`application/main_web.py` file for start server instead `uvicorn` load.
`application/common` folder for common stuff like utils, constants, etc.
`application/dbs` folder for db adapters.
`application/domain` folder for business logic of application.
`application/server` folder for web server logic of application.
`tests` folder for tests.

# Run api
cd application
uvicorn server.app:app --host $API_HOST --port=$API_PORT

# Build Docker
from project root
docker build . -f ./docker/application/Dockerfile  -t url-shortener:latest
docker-compose  -f docker/docker-compose-dev.yml
