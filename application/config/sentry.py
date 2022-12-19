"""Config of apps"""
from pydantic import BaseSettings, Field


class SentrySettings(BaseSettings):  # TODO: not used fields
    """Application env values"""

    dsn: str = Field('', env='SENTRY_DSN')
