from fastapi import APIRouter, Depends, HTTPException

from domain.goods import CategoryName, ProductID, ProductInfoService
from .deps import get_product_parser_service
from .schemas import ProductInfoResponse

router = APIRouter()


@router.get('/category/{category_name}', response_model=ProductInfoResponse)
async def get_product_category_info(
    category: CategoryName,
    product_info_service: ProductInfoService = Depends(get_product_parser_service),
) -> ProductInfoResponse:
    """
    Get a product info by product name.
    """
    product_info_entities = await product_info_service.find_category_products(
        category=category
    )
    if not product_info_entities:
        raise HTTPException(status_code=404, detail='Not found')
    return ProductInfoResponse(data=product_info_entities)


@router.get('/{product_id}', response_model=ProductInfoResponse)
async def get_product_info(
    product_id: ProductID,
    product_info_service: ProductInfoService = Depends(get_product_parser_service),
) -> ProductInfoResponse:
    """
    Get a product info by product name.
    """
    product_info_entity = await product_info_service.get_product(product_id=product_id)
    if not product_info_entity:
        raise HTTPException(status_code=404, detail='Not found')
    return ProductInfoResponse(data=[product_info_entity])
