"""Config of apps"""
from pydantic import BaseSettings, Field


class SentrySettings(BaseSettings):
    """Application env values"""

    dsn: str = Field('', env='SENTRY_DSN')
