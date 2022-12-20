"""Config of apps"""
from pydantic import BaseSettings
from pydantic import Field


class SentrySettings(BaseSettings):  # TODO: not used fields
    """Application env values"""

    dsn: str = Field("", env="SENTRY_DSN")
