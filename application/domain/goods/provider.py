"""
Providers base entities.
"""
import itertools
import urllib.parse
from abc import ABCMeta, abstractmethod
from typing import Optional

from loguru import logger
from pydantic import HttpUrl, parse_obj_as
from pydantic import ValidationError
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from clients.parser import BaseParser
from common.errors import ProviderError
from common.utils import async_wrapper, retry_by_exception
from .entities import ProductEntity
from .types import ProductID, CategoryName, ProductName


class Provider(metaclass=ABCMeta):
    """
    Provider interface class.
    """

    @abstractmethod
    async def get_product(self, product_id: ProductID) -> ProductEntity:
        """
        Get product data entity by product id.
        """


class SberSuperMarketProvider(Provider):
    """
    Provider interface class.
    """

    product_name_path = {By.CLASS_NAME: 'pdp-header__title', By.XPATH: '//header/h1'}
    product_description_path = {By.CLASS_NAME: 'product-description'}
    product_price_path = {By.CLASS_NAME: 'pdp-sales-block__price-final'}
    product_images_path = {
        By.XPATH: '//li[@class="pdp-reviews-gallery-preview__item"]/img[@class="lazy-img"]',
        By.CLASS_NAME: 'slide__image',
    }
    product_specs_names_path = {By.CLASS_NAME: 'pdp-specs__item-name'}
    product_specs_values_path = {By.CLASS_NAME: 'pdp-specs__item-value'}
    product_categories_path = {By.CLASS_NAME: 'breadcrumb-item'}

    def __init__(self, parser: BaseParser, base_url: HttpUrl) -> None:
        self.parser = parser
        self.base_url = base_url

    async def get_product(self, product_id: ProductID) -> ProductEntity:
        """
        Get product entity by product id.
        """
        return await retry_by_exception(exceptions=ProviderError, max_tries=3)(
            async_wrapper(self._get_product)
        )(product_id)

    def _get_product(self, product_id: ProductID) -> ProductEntity:
        """
        Get product entity by product id sync version.
        """

        self._get_product_page(product_id)
        # TODO: Sometimes drives go down - maybe better decision to use BeautifulSoup with self.parser.page_source
        logger.info(f'Start getting info for product with product id: {product_id}')
        name = self._get_product_name()
        description = self._get_product_description()
        price = self._get_product_price()
        images = self._get_product_images()
        specifications = self._get_product_specifications()
        categories = self._get_product_categories()

        return self._make_product_entity(
            product_id=product_id,
            name=name,
            description=description,
            price=price,
            images=images,
            specifications=specifications,
            categories=categories,
        )

    @staticmethod
    def _make_product_entity(
        product_id: ProductID,
        name: Optional[ProductName],
        description: Optional[str],
        price: Optional[str],
        images: list[dict[str, str]],
        specifications: list[dict[str, str]],
        categories: list[CategoryName],
    ) -> ProductEntity:
        try:
            product = ProductEntity(
                product_id=product_id,
                name=name,
                description=description,
                price=price,
                images=images,
                specifications=specifications,
                categories=categories,
            )
        except ValidationError as err:
            logger.warning(
                f"""Get exception for ProductEntity {err}, with data: {
                        dict(
                            product_id=product_id,
                            name=name,
                            description=description,
                            price=price,
                            images=images,
                            specifications=specifications,
                            categories=categories
                        )
                    }
                """
            )
            raise ProviderError from err
        logger.debug(
            f'Got getting info for product with product id {product_id}: \n {product.json()}'
        )
        if product.is_empty:
            raise ProviderError(f'Product data for product id: {product_id} is empty')
        return product

    def _get_product_page(self, product_id: ProductID):
        """
        Get product page entity by product id.
        """
        product_data_url = parse_obj_as(
            HttpUrl,
            urllib.parse.urljoin(str(self.base_url), f'catalog/?q={product_id}'),
        )
        self.parser.get_page(urllib.parse.urljoin(self.base_url, product_data_url))

    def _get_elements_data(self, path_dict: dict[By, str]) -> list[WebElement]:
        for key, value in path_dict.items():
            if data := self.parser.get_elements(by=key, name=value):
                return data
        return []

    def _get_product_name(self) -> ProductName:
        """
        Get product name.
        """
        if name_data := self._get_elements_data(self.product_name_path):
            return ProductName(name_data[0].text)
        return ProductName('')

    def _get_product_description(self) -> str:
        """
        Get product description.
        """
        if description_data := self._get_elements_data(self.product_description_path):
            return description_data[0].text
        return ''

    def _get_product_price(self) -> str:
        """
        Get product description.
        """
        if price_data := self._get_elements_data(self.product_price_path):
            price = price_data[0].text.replace(' ', '').replace('₽', '')
            return price if price else '0'
        return '0'

    def _get_product_images(self) -> list[dict[str, str]]:
        """
        Get product images.
        """
        if images_data := self._get_elements_data(self.product_images_path):
            images = [
                {'name': img.get_property('alt'), 'url': img.get_property('src')}
                for img in images_data
                if img.get_property('src')
            ]
            return images
        return []

    def _get_product_specifications(self) -> list[dict[str, str]]:
        """
        Get product metadata.
        """
        if not (specs_names := self._get_elements_data(self.product_specs_names_path)):
            return []
        if not (
            specs_values := self._get_elements_data(self.product_specs_values_path)
        ):
            return []

        names = [key.text for key in specs_names]
        values = [key.text for key in specs_values]
        specs_data = [
            {'name': key, 'value': value}
            for key, value in itertools.zip_longest(names, values, fillvalue='')
            if key
        ]
        return specs_data

    def _get_product_categories(self) -> list[CategoryName]:
        """
        Get product metadata.
        """
        if categories_data := self._get_elements_data(self.product_categories_path):
            categories = [
                CategoryName(category.text)
                for category in categories_data
                if category.text
            ]
            return categories
        return []
