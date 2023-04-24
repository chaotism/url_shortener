import hashlib
from decimal import Decimal
from typing import Optional
from urllib.parse import urljoin

from pydantic import validator, HttpUrl, Field

from ..entities import Entity, EncodedModel
from .types import ProductID, ProductName, CategoryName


class ProductImage(EncodedModel):
    name: str
    url: HttpUrl


class ProductAttribute(EncodedModel):
    name: str
    value: str


class ProductEntity(Entity):
    product_id: ProductID = Field(alias='goodsId', description='Штрихкод')
    name: ProductName
    price: Decimal

    categories: list[CategoryName]
    images: list[ProductImage]
    specifications: list[ProductAttribute]

    @property
    def is_empty(self) -> bool:
        if not any([self.name, self.price, self.categories, self.images, self.specifications]):
            return True
        return False