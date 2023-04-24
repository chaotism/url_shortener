"""Config of application"""
from .application import ApplicationSettings
from .auth import AuthSettings
from .client import SberSuperMarketParserSettings
from .db import MongodbSettings
from .openapi import OpenAPISettings
from .sentry import SentrySettings


application_config = ApplicationSettings()
auth_config = AuthSettings.generate()
mongodb_config = MongodbSettings.generate()
openapi_config = OpenAPISettings.generate()
sentry_config = SentrySettings()
parser_config = SberSuperMarketParserSettings.generate()
