from decimal import Decimal

from pydantic import HttpUrl, Field

from .types import ProductID, ProductName, CategoryName
from ..entities import Entity, EncodedModel


class ProductImage(EncodedModel):
    name: str
    url: HttpUrl


class ProductAttribute(EncodedModel):
    name: str
    value: str


class ProductEntity(Entity):
    product_id: ProductID = Field(description='Штрихкод')
    name: ProductName
    price: Decimal

    categories: list[CategoryName]
    images: list[ProductImage]
    specifications: list[ProductAttribute]

    @property
    def is_empty(self) -> bool:
        if not any(
            [self.name, self.price, self.categories, self.images, self.specifications]
        ):
            return True
        return False
