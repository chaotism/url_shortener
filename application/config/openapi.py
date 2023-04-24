"""OpenAPI-schema"""
from pydantic import AnyHttpUrl, BaseSettings, Field
from poetry.core.constraints.version import Version

OPENAPI_API_NAME = 'The best API ever'
OPENAPI_API_VERSION = '0.0.1'
OPENAPI_API_DESCRIPTION = 'API for humans'
OPENAPI_SERVER_NAME = 'http://short.edu'


class OpenAPISettings(BaseSettings):
    name: str = Field(default=OPENAPI_API_NAME, env='OPENAPI_NAME')
    version: str = Field(
        default=Version.parse(OPENAPI_API_VERSION).text, env='OPENAPI_VERSION'
    )
    description: str = Field(default=OPENAPI_API_DESCRIPTION, env='OPENAPI_DESCRIPTION')
    server_name: AnyHttpUrl = Field(
        default=OPENAPI_SERVER_NAME, env='OPENAPI_SERVERNAME'
    )

    @classmethod
    def generate(cls):
        return OpenAPISettings(
            name=OPENAPI_API_NAME,
            version=OPENAPI_API_VERSION,
            description=OPENAPI_API_DESCRIPTION,
            server_name=OPENAPI_SERVER_NAME,
        )
