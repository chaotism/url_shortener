from pydantic import BaseModel

from domain.goods import ProductID, ProductEntity
from domain.entities import EncodedModel


# Properties to receive on creation
class ProductInfoRequest(BaseModel):
    product_id: ProductID


# Properties to return to client
class ProductInfoResponse(EncodedModel):
    data: list[ProductEntity]
