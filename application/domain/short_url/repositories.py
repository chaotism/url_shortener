from abc import ABCMeta, abstractmethod
from contextlib import asynccontextmanager
from typing import List

from fastapi.encoders import jsonable_encoder
from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from ..errors import EntityError, RepositoryError
from ..types import Repository
from .entities import ShortUrlEntity
from .types import UrlID, UrlName

URL_COLLECTION_NAME = 'urls'


class UrlRepository(Repository):
    __metaclass__ = ABCMeta

    @abstractmethod
    async def get_count(self) -> int:
        pass

    @abstractmethod
    async def get_by_id(self, instance_id: UrlID) -> ShortUrlEntity:
        pass

    @abstractmethod
    async def find_by_name(self, name: UrlName) -> List[ShortUrlEntity]:
        pass

    @abstractmethod
    async def insert(self, instance: ShortUrlEntity) -> UrlID:
        pass

    @abstractmethod
    async def update(self, instance: ShortUrlEntity) -> None:
        pass

    @abstractmethod
    async def delete(self, instance: ShortUrlEntity) -> None:
        pass

    @abstractmethod
    @asynccontextmanager
    async def atomic(self):
        pass


class MotorUrlRepository(UrlRepository):
    buff_size: int = 1000

    collection_name = URL_COLLECTION_NAME

    def __init__(self, client: AsyncIOMotorClient, db: AsyncIOMotorDatabase):
        self.client = client
        self.db = db
        self.collection = getattr(self.db, self.collection_name)
        self._create_indexes()

    def _create_indexes(self):
        logger.info('Creating indexes')
        self.collection.create_index('name', unique=True, sparse=True, background=True)

    async def get_count(self) -> int:
        return self.collection.count_documents({})

    async def get_by_id(self, instance_id: UrlID) -> ShortUrlEntity:
        url = await self.collection.find_one({'_id': instance_id})
        if url is None:
            raise RepositoryError(
                f'Cannot find object in collection {self.collection} by id {instance_id}'
            )
        return ShortUrlEntity(**url)

    async def find_by_name(self, name: UrlName) -> List[ShortUrlEntity]:
        urls_data_cursor = self.collection.find({'name': name})
        urls_data = [
            data for data in await urls_data_cursor.to_list(length=self.buff_size)
        ]
        if not urls_data:
            return []
        return [ShortUrlEntity(**data) for data in urls_data]

    async def insert(self, instance: ShortUrlEntity) -> UrlID:
        data = jsonable_encoder(instance, by_alias=True)
        data.pop('_id')
        result = await self.collection.insert_one(data)
        return result.inserted_id

    async def update(self, instance: ShortUrlEntity) -> None:
        instance_id = instance.get_id()
        if not instance_id:
            raise EntityError('Null id')
        data = jsonable_encoder(instance, by_alias=True)
        data.pop('_id')
        await self.collection.update_one({'_id': instance_id}, {'$set': data})

    async def delete(self, instance: ShortUrlEntity) -> None:
        instance_id = instance.get_id()
        if not instance_id:
            raise EntityError('Null id')
        await self.collection.delete_one({'_id': instance_id})

    @asynccontextmanager
    async def atomic(self):
        async with await self.client.start_session() as s:
            async with s.start_transaction():
                yield
