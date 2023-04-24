from typing import Optional

from config.db import MongodbSettings
from common.errors import DatabaseError
from loguru import logger
from motor import motor_asyncio
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase


class MongoMotorAdapter:
    config: Optional[MongodbSettings] = None  # TODO: could remove (its for debug only)
    client: Optional[AsyncIOMotorClient] = None
    db: Optional[AsyncIOMotorDatabase] = None

    @property
    def is_inited(self):
        return (
            self.config is not None and self.client is not None and self.db is not None
        )

    async def get_db(self):
        if not self.is_inited:
            raise DatabaseError(f'{self.__class__.__name__} is not inited')
        return self.db

    async def get_client(self):
        if not self.is_inited:
            raise DatabaseError(f'{self.__class__.__name__} is not inited')
        return self.client

    async def init(self, config: MongodbSettings):
        if self.is_inited:
            logger.info('Already inited')
            return
        logger.info('Start opening connection.....')
        self.config = config
        self.client = motor_asyncio.AsyncIOMotorClient(self.config.uri)
        self.db = self.client[self.config.db]
        logger.info('Connection open')

    async def close_connections(self):
        if not self.is_inited:
            logger.warning(f'{self.__class__.__name__} is not inited')
            return
        logger.info('Start closing connection...')
        self.client.close()
        logger.info('Connection closed')

    async def auth_mongo(self):
        if not self.is_inited:
            raise DatabaseError(f'{self.__class__.__name__} is not inited')
        if self.config.username is not None:
            logger.info('Find mongo username, try to get authentication')
            await self.db.authenticate(self.config.username, self.config.password)


async def get_mongo_client() -> AsyncIOMotorClient:
    return await mongo_adapter.get_client()


async def get_mongo_db() -> AsyncIOMotorClient:
    return await mongo_adapter.get_db()


mongo_adapter = MongoMotorAdapter()
