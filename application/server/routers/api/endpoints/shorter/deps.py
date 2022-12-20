from dbs.mongo import get_mongo_client
from dbs.mongo import get_mongo_db
from domain.short_url import MotorUrlRepository
from domain.short_url import UrlShorterService


async def get_url_shorter_service() -> UrlShorterService:
    client = await get_mongo_client()
    db = await get_mongo_db()
    return UrlShorterService(MotorUrlRepository(client=client, db=db))
