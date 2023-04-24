from typing import Optional

from domain.goods import ProductID, ProductEntity
from pydantic import BaseModel


# Properties to receive on creation
class ProductInfoRequest(BaseModel):
    product_id: ProductID


# Properties to return to client
class ProductInfoResponse(BaseModel):
    data: list[ProductEntity]
