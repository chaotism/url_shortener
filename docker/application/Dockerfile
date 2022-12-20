FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

ENV SERVICE_NAME "fast-url-shortener"
ENV USER_HOME "/opt/$SERVICE_NAME"
ENV APP_PATH "$USER_HOME/application"
ENV WEB_PORT 8888


RUN set -ex && \
    mkdir -p  $USER_HOME


COPY ./  $USER_HOME


WORKDIR $USER_HOME


RUN set -ex && \
    pip install poetry && \
    poetry install -n


WORKDIR $APP_PATH


# Run FastApi
CMD [ "sh", "-c", "uvicorn ${APP_PATH}/server/app:app --host=0.0.0.0 --port=${WEB_PORT}"]
