from typing import Optional

from pydantic import ValidationError

from ..errors import EntityError, ServiceError
from ..types import Service
from .entities import ShortUrlEntity
from .repositories import UrlRepository
from .types import FullUrl, UrlName


class UrlShorterService(Service):
    def __init__(self, url_repo: UrlRepository) -> None:
        self.url_repo = url_repo

    @staticmethod
    def _make_url_entity(url: FullUrl, name: Optional[UrlName]) -> ShortUrlEntity:
        try:
            return ShortUrlEntity(full_url=url, name=name)
        except (EntityError, ValidationError) as err:  # TODO: remove ValidationError
            raise ServiceError('Get error for making entity') from err

    async def register_url(
        self, url: FullUrl, name: Optional[UrlName] = None
    ) -> ShortUrlEntity:
        url_data = dict(url=url, name=None)
        if name is not None:  # for manual name input
            if exist_short_url := await self.get_url(name):
                if exist_short_url.full_url == url:
                    return exist_short_url
                raise ServiceError(
                    f'Short url with this name {name} is already exists with different url: {exist_short_url.full_url}'
                )
            url_data['name'] = name

        url_entity = self._make_url_entity(**url_data)
        async with self.url_repo.atomic():  # TODO: make it simpler
            if exist_short_url := await self.get_url(name):
                url_entity.id = exist_short_url.get_id()
                await self.url_repo.update(url_entity)
                return url_entity

            repo_url_id = await self.url_repo.insert(url_entity)
            url_entity.id = repo_url_id
            return url_entity

    async def get_url(self, name: UrlName) -> Optional[ShortUrlEntity]:
        urls = await self.url_repo.find_by_name(name)
        if not urls:
            return None
        if len(urls) > 1:
            raise ServiceError(f'Find more than one url by name {name}: {urls}')
        return urls[0]

    async def remove_url(self, name: UrlName):
        url = await self.get_url(name)
        if not url:
            return None
        await self.url_repo.delete(url.get_id())

    async def have_urls(self) -> bool:
        return await self.url_repo.get_count() > 0
