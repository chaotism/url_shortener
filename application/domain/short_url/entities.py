import hashlib
from typing import Optional
from urllib.parse import urljoin

from pydantic import validator

from ..entities import Entity
from .types import FullUrl, UrlName


class ShortUrlEntity(Entity):
    full_url: FullUrl
    name: Optional[UrlName]

    def generate_short_url(self, host: str):
        return urljoin(host, self.name)

    @validator('name', pre=True)
    def fulfill_empty_name(cls, v, values):
        if v is None:
            try:
                v = hashlib.sha256()
                v.update(values['full_url'].encode())
                return v.hexdigest()[
                    : UrlName.max_length
                ]  # TODO: change hashing method to shorter
            except Exception as err:  # TODO: make strict
                raise ValueError('Name generation error') from err
        return v
