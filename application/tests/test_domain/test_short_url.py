from contextlib import asynccontextmanager
from typing import List

import pytest
from bson import ObjectId
from domain.errors import EntityError, ServiceError
from domain.short_url import (
    ShortUrlEntity,
    UrlID,
    UrlName,
    UrlRepository,
    UrlShorterService,
)
from domain.types import PDObjectId


class TestUrlEntity:
    """
    tests with User fields validation
    """

    @pytest.mark.parametrize(
        'input_url, input_name, result_name',
        (
            (
                'http://looooong.com/somepath',
                None,
                '32533af22a12004e6654effbb596c715d1fb1c56127e7c8973',
            ),
            ('http://looooong.com/somepath', 'POTATO', 'POTATO'),
        ),
    )
    def test_fulfill_name(self, input_url, input_name, result_name):
        entity = ShortUrlEntity(full_url=input_url, name=input_name)
        assert str(entity.name) == result_name

    def test_generate_short_url(self):
        entity = ShortUrlEntity(full_url='http://looooong.com/somepath', name='POTATO')
        assert entity.generate_short_url('http://0.0.0.0') == 'http://0.0.0.0/POTATO'


class TestUrlShorterService:
    host = 'http://short.com'

    @pytest.fixture()
    def simple_url(self):
        return ShortUrlEntity(
            _id=ObjectId(),
            full_url='http://looooong.com/somepath',
            name='MY-NEW-WS',
        )

    @pytest.fixture(scope='class')
    def fake_url_repo(self):
        class FakUrlRepository(UrlRepository):
            data: dict[PDObjectId, ShortUrlEntity] = {}

            async def get_count(self) -> int:
                return len(self.data)

            async def get_by_id(self, instance_id: UrlID) -> ShortUrlEntity:
                return self.data.get(instance_id)

            async def find_by_name(self, name: UrlName) -> List[ShortUrlEntity]:
                return [entity for entity in self.data.values() if entity.name == name]

            async def insert(self, instance: ShortUrlEntity) -> UrlID:
                instance.set_id(PDObjectId())
                self.data[instance.get_id()] = instance
                return instance.get_id()

            async def update(self, instance: ShortUrlEntity) -> None:
                if instance.get_id():
                    self.data[instance.get_id()] = instance
                raise EntityError('Null id')

            async def delete(self, instance: ShortUrlEntity) -> None:
                if instance.get_id():
                    self.data.pop(instance.get_id())
                raise EntityError('Null id')

            @asynccontextmanager
            async def atomic(self):
                try:
                    yield
                finally:
                    pass

        return FakUrlRepository()

    @pytest.mark.parametrize(
        argnames='full_url,name,result,exception',
        argvalues=[
            (
                'http://looooong.com/somepath',
                None,
                'http://short.com/32533af22a12004e6654effbb596c715d1fb1c56127e7c8973',
                None,
            ),
            (
                'http://looooong.com/somepath',
                'MY-NEW-WS',
                'http://short.com/MY-NEW-WS',
                None,
            ),
            ('http://looooong.com/somepath', 'POTATO', 'http://short.com/POTATO', None),
            ('http://looooong.com/somepath', 'POTATO', 'http://short.com/POTATO', None),
            (
                'http://looooong.com/anotherpath',
                'POTATO',
                None,
                ServiceError(
                    'Short url with this name POTATO is already exists with different url: http://looooong.com/somepath'
                ),
            ),
            (
                'http://looooong.com/anotherpath',
                'POTAT' * 10 + '0',
                None,
                ServiceError('Get error for making entity'),
            ),
        ],
        ids=[
            'empty',
            'MY-NEW-WS',
            'POTATO',
            'POTATO-duplicate',
            'POTATO-duplicate-different-url',
            'Long-name',
        ],
    )
    @pytest.mark.asyncio
    async def test_register_url(self, fake_url_repo, full_url, name, result, exception):
        url_shorter_service = UrlShorterService(fake_url_repo)
        if exception:
            with pytest.raises(type(exception)) as err:
                await url_shorter_service.register_url(url=full_url, name=name)
            assert str(exception) == str(err.value)
            return
        short_url_entity = await url_shorter_service.register_url(
            url=full_url, name=name
        )
        assert short_url_entity.generate_short_url(self.host) == result


class TestUserRepository:  # TODO: write test of base method of repos
    pass
