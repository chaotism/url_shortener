from typing import Optional

from domain.short_url import FullUrl, ShortUrl, UrlName
from pydantic import BaseModel


# Properties to receive on creation
class ShortUrlCreateRequest(BaseModel):
    full_url: FullUrl
    name: Optional[UrlName]


# Properties to return to client
class StoredShortUrlResponse(BaseModel):
    short_url: ShortUrl


class StoredFullUrlResponse(BaseModel):
    full_url: FullUrl
