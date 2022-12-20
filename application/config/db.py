"""Config of DBS"""
from typing import Optional

from pydantic import BaseSettings, Field

from .application import ApplicationSettings

MONGO_DEFAULT_DB_URI = 'mongodb://localhost:27017'
MONGO_DEFAULT_DB_NAME = 'sf'
MONGO_DEFAULT_DB_TEST_NAME = 'sf-test'


class MongodbSettings(BaseSettings):
    """Mongodb env values"""

    uri: str = Field(default=MONGO_DEFAULT_DB_URI, env='MONGO_URI')
    db: str = Field(default=MONGO_DEFAULT_DB_NAME, env='MONGO_DB')

    username: Optional[str] = Field(default=None, env='MONGO_USERNAME')
    password: Optional[str] = Field(default=None, env='MONGO_PASSWORD')

    @classmethod
    def generate(cls):
        """Generate MongoDD settings (with sqlite if tests)"""
        application_settting = ApplicationSettings()
        if application_settting.is_test:
            return MongodbSettings(db=MONGO_DEFAULT_DB_TEST_NAME)
        return MongodbSettings()
