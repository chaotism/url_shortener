from datetime import date
from datetime import datetime
from datetime import time
from datetime import timedelta
from decimal import Decimal
from enum import Enum
from types import GeneratorType
from typing import Optional
from uuid import UUID

from bson import ObjectId
from pydantic import BaseModel
from pydantic import Field


class PDObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class EncodedModel(BaseModel):
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            UUID: str,
            datetime: lambda dt: dt.isoformat(),
            date: lambda d: d.isoformat(),
            time: lambda t: t.isoformat(),
            timedelta: lambda td: td.total_seconds(),
            bytes: lambda o: o.decode(),
            set: list,
            frozenset: list,
            GeneratorType: list,
            Decimal: float,
            Enum: lambda v: v.value,
        }


class Entity(EncodedModel):
    id: Optional[PDObjectId] = Field(alias="_id")
    created_at: Optional[datetime] = Field(default_factory=lambda: datetime.now())

    def get_id(self):
        return self.id

    def set_id(self, id: PDObjectId):
        self.id = id

    def dict(self, *args, **kwargs):
        hidden_fields = {
            attribute_name
            for attribute_name, model_field in self.__fields__.items()
            if model_field.field_info.extra.get("hidden") is True
        }
        kwargs.setdefault("exclude", hidden_fields)
        return super().dict(*args, **kwargs)


class DAO:
    pass


class Service:
    pass


class Repository:
    pass
