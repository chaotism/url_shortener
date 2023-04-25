from typing import NewType

ProductID = NewType('ProductID', str)


class ProductName(str):
    max_length = 512

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if len(v) > ProductName.max_length:
            raise ValueError('Product name too long')
        return v

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            type='string',
            examples=['POTATO', 'MY-NEW-WS', 'shampoo'],
        )


class CategoryName(str):  # TODO: copypaste
    max_length = 512

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if len(v) > ProductName.max_length:
            raise ValueError('Category name too long')
        return v

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            type='string',
            examples=['POTATO', 'MY-NEW-WS', 'shampoo'],
        )
