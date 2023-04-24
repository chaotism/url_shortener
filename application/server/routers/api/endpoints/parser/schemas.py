from pydantic import BaseModel

from domain.goods import ProductID, ProductEntity


# Properties to receive on creation
class ProductInfoRequest(BaseModel):
    product_id: ProductID


# Properties to return to client
class ProductInfoResponse(BaseModel):
    data: list[ProductEntity]
