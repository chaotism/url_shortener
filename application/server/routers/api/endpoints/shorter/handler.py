from typing import Any

from config import openapi_config
from domain.errors import ServiceError
from domain.short_url import ShortUrlEntity
from domain.short_url import UrlName
from domain.short_url import UrlShorterService
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from .deps import get_url_shorter_service
from .schemas import ShortUrlCreate
from .schemas import StoredFullUrl
from .schemas import StoredShortUrl

router = APIRouter()


@router.get("/{url_name}", response_model=StoredFullUrl)
async def get_url(
    url_name: UrlName, url_service: UrlShorterService = Depends(get_url_shorter_service)
) -> StoredFullUrl:  # TODO: migrate to redirect
    """
    Get a specific url by name.
    """
    url_entity = await url_service.get_url(name=url_name)
    if not url_entity:
        raise HTTPException(status_code=404, detail="Not found")
    return StoredFullUrl(full_url=url_entity.full_url)


@router.post("/", response_model=StoredShortUrl)
async def create_url(
    *,
    url_service: UrlShorterService = Depends(get_url_shorter_service),
    url_in: ShortUrlCreate
) -> StoredShortUrl:
    """
    Create new short url.
    """
    try:
        register_url_entity = await url_service.register_url(
            url=url_in.full_url, name=url_in.name
        )
        short_url = register_url_entity.generate_short_url(openapi_config.server_name)
        return StoredShortUrl(short_url=short_url)
    except ServiceError as err:
        raise HTTPException(
            status_code=400,
            detail=str(err),
        )
