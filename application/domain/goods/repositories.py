from abc import ABCMeta, abstractmethod
from contextlib import asynccontextmanager
from typing import List

from loguru import logger
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from ..errors import EntityError, RepositoryError
from ..types import Repository, PDObjectId
from .entities import ProductEntity
from .types import ProductID, ProductName, CategoryName

PRODUCT_COLLECTION_NAME = 'goods'


class ProductRepository(Repository):
    __metaclass__ = ABCMeta

    @abstractmethod
    async def get_count(self) -> int:
        pass

    @abstractmethod
    async def get_by_id(
        self, instance_id: PDObjectId
    ) -> ProductEntity:  # TODO: remove it
        pass

    @abstractmethod
    async def find_by_product_id(self, product_id: ProductID) -> List[ProductEntity]:
        pass

    @abstractmethod
    async def find_by_name(self, name: ProductName) -> List[ProductEntity]:
        pass

    @abstractmethod
    async def find_by_category(self, category: CategoryName) -> List[ProductEntity]:
        pass

    @abstractmethod
    async def insert(self, instance: ProductEntity) -> PDObjectId:
        pass

    @abstractmethod
    async def update(self, instance: ProductEntity) -> None:
        pass

    @abstractmethod
    async def delete(self, instance: ProductEntity) -> None:
        pass

    @abstractmethod
    @asynccontextmanager
    async def atomic(self):
        pass


class MotorProductRepository(ProductRepository):
    buff_size: int = 1000

    collection_name = PRODUCT_COLLECTION_NAME

    def __init__(self, client: AsyncIOMotorClient, db: AsyncIOMotorDatabase):
        self.client = client
        self.db = db
        self.collection = getattr(self.db, self.collection_name)
        self._create_indexes()

    def _create_indexes(self):  # TODO: move to tasks
        logger.info('Creating indexes')
        self.collection.create_index(
            'product_id', unique=True, sparse=True, background=True
        )

    async def get_count(self) -> int:
        return self.collection.count_documents({})

    async def get_by_id(self, instance_id: PDObjectId) -> ProductEntity:
        product = await self.collection.find_one({'_id': instance_id})
        if product is None:
            raise RepositoryError(
                f'Cannot find object in collection {self.collection} by id {instance_id}'
            )
        return ProductEntity(**product)

    async def find_by_product_id(self, product_id: ProductID) -> List[ProductEntity]:
        products_data_cursor = self.collection.find({'product_id': product_id})
        products_data = [
            data for data in await products_data_cursor.to_list(length=self.buff_size)
        ]
        if not products_data:
            return []
        return [ProductEntity(**data) for data in products_data]

    async def find_by_name(self, name: ProductName) -> List[ProductEntity]:
        products_data_cursor = self.collection.find({'name': name})
        products_data = [
            data for data in await products_data_cursor.to_list(length=self.buff_size)
        ]
        if not products_data:
            return []
        return [ProductEntity(**data) for data in products_data]

    async def find_by_category(self, category: CategoryName) -> List[ProductEntity]:
        products_data_cursor = self.collection.find(
            {'category': {'$elemMatch': {'$in': [category]}}}
        )
        products_data = [
            data for data in await products_data_cursor.to_list(length=self.buff_size)
        ]
        if not products_data:
            return []
        return [ProductEntity(**data) for data in products_data]

    async def insert(self, instance: ProductEntity) -> PDObjectId:
        data = jsonable_encoder(instance, by_alias=True)
        data.pop('_id')
        result = await self.collection.insert_one(data)
        return result.inserted_id

    async def update(self, instance: ProductEntity) -> None:
        instance_id = instance.get_id()
        if not instance_id:
            raise EntityError('Null id')
        data = jsonable_encoder(instance, by_alias=True)
        data.pop('_id')
        await self.collection.update_one({'_id': instance_id}, {'$set': data})

    async def delete(self, instance: ProductEntity) -> None:
        instance_id = instance.get_id()
        if not instance_id:
            raise EntityError('Null id')
        await self.collection.delete_one({'_id': instance_id})

    @asynccontextmanager
    async def atomic(self):
        async with await self.client.start_session() as s:
            async with s.start_transaction():
                yield
