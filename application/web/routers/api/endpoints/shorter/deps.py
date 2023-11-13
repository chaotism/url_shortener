from dbs.mongo import get_mongo_client, get_mongo_db
from domain.short_url import MotorUrlRepository, UrlShorterService


async def get_url_shorter_service() -> UrlShorterService:
    client = await get_mongo_client()
    db = await get_mongo_db()
    return UrlShorterService(url_repo=MotorUrlRepository(client=client, db=db))
