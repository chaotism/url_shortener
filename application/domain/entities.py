from datetime import datetime, date, time, timedelta
from bson import ObjectId
from decimal import Decimal
from enum import Enum
from types import GeneratorType
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from domain.types import PDObjectId


class EncodedModel(BaseModel):
    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        json_encoders = (
            {  # possible to remove and use jsonable_encoder from fastapi.encoders
                UUID: str,
                ObjectId: str,
                PDObjectId: str,
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
        )


class Entity(EncodedModel):
    id: Optional[PDObjectId] = Field(alias='_id')
    created_at: Optional[datetime] = Field(default_factory=lambda: datetime.utcnow())
    modified_at: Optional[datetime] = Field(default_factory=lambda: datetime.utcnow())

    def get_id(self):
        return self.id

    def set_id(self, id: PDObjectId):
        self.id = id

    def set_modified_at(self):
        self.modified_at = datetime.utcnow()

    def dict(self, *args, **kwargs):
        hidden_fields = {
            attribute_name
            for attribute_name, model_field in self.__fields__.items()
            if model_field.field_info.extra.get('hidden') is True
        }
        kwargs.setdefault('exclude', hidden_fields)
        return super().dict(*args, **kwargs)
