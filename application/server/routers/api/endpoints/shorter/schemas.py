from typing import Optional

from domain.short_url import FullUrl, ShortUrl, UrlName
from pydantic import BaseModel


# Properties to receive on creation
class ShortUrlCreate(BaseModel):
    full_url: FullUrl
    name: Optional[UrlName]


# Properties to return to client
class StoredShortUrl(BaseModel):
    short_url: ShortUrl


class StoredFullUrl(BaseModel):
    full_url: FullUrl
