"""OpenAPI-schema"""
from pydantic import AnyHttpUrl, BaseSettings

OPENAPI_API_NAME = 'The best API ever'
OPENAPI_API_VERSION = '0.0.1 beta'
OPENAPI_API_DESCRIPTION = 'API for humans'
OPENAPI_SERVER_NAME = 'http://short.com'  # TODO: rename


class OpenAPISettings(BaseSettings):
    name: str
    version: str
    description: str
    server_name: AnyHttpUrl

    @classmethod
    def generate(cls):
        return OpenAPISettings(
            name=OPENAPI_API_NAME,
            version=OPENAPI_API_VERSION,
            description=OPENAPI_API_DESCRIPTION,
            server_name=OPENAPI_SERVER_NAME,
        )
