from typing import Optional

from loguru import logger

from common.errors import ProviderError, NotFoundError
from common.utils import duration_measure
from .entities import ProductEntity
from .provider import Provider
from .repositories import ProductRepository
from .types import ProductID, CategoryName
from ..errors import ServiceError
from ..types import Service


class ProductInfoService(Service):
    def __init__(
        self, product_repo: ProductRepository, product_provider: Provider
    ) -> None:
        self.product_repo = product_repo
        self.product_provider = product_provider

    async def register_provider_product_info(  # TODO: add seed products
        self, product_id: ProductID
    ) -> ProductEntity:
        try:
            product_data = await self.product_provider.get_product(product_id)
        except ProviderError as err:
            logger.warning(f'Get provider error {err} for product id {product_id} ')
            raise NotFoundError(f'Cannot find information for product id: {product_id}')
        id_ = await self.product_repo.insert(product_data)
        product_db_data = await self.product_repo.get_by_id(id_)
        return product_db_data

    async def find_category_products(
        self, category: CategoryName
    ) -> list[ProductEntity]:
        products = await self.product_repo.find_by_category(category)
        if not products:
            return []
        return products

    @duration_measure
    async def get_product(self, product_id: ProductID) -> Optional[ProductEntity]:
        products = await self.product_repo.find_by_product_id(product_id)
        logger.debug(f'Get {products} by key {product_id}')
        if not products:
            try:
                return await self.register_provider_product_info(product_id)
            except NotFoundError as err:
                logger.warning(str(err))
                return None
        if len(products) > 1:
            raise ServiceError(
                f'Find more than one product by product_id {product_id}: {products}'
            )
        return products[0]

    async def remove_product(
        self, product_id: ProductID
    ) -> Optional[ProductEntity]:  # TODO: not used
        products = await self.get_product(product_id)
        if not products:
            return None
        await self.product_repo.delete(products.get_id())

    async def have_products(self) -> bool:  # TODO: not used
        return await self.product_repo.get_count() > 0
