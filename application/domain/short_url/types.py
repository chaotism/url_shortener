from typing import NewType

from pydantic import AnyHttpUrl

from ..types import PDObjectId

UrlID = NewType('UrlID', PDObjectId)


class UrlName(str):
    max_length = 50

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if len(v) > UrlName.max_length:
            raise ValueError('Url name too long')
        return v

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            type='string',
            examples=['POTATO', 'MY-NEW-WS'],
        )


class FullUrl(AnyHttpUrl):
    """
    # TODO: add additional pydantic validation into field
    """


class ShortUrl(AnyHttpUrl):
    """
    # TODO: add additional pydantic validation into field
    """
