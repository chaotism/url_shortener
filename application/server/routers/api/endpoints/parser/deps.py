from dbs.mongo import get_mongo_client, get_mongo_db
from clients import parser_client
from domain.goods import (
    MotorProductRepository,
    SberSuperMarketProvider,
    ProductInfoService,
)
from config import parser_config


async def get_product_parser_service() -> ProductInfoService:
    client = await get_mongo_client()
    db = await get_mongo_db()
    return ProductInfoService(
        product_repo=MotorProductRepository(client=client, db=db),
        product_provider=SberSuperMarketProvider(
            parser=parser_client, base_url=parser_config.url
        ),
    )
