from typing import TypeVar
from uuid import UUID

import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class FastModel(BaseModel):

    class Config:
        orm_mode = True

    class Meta:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class BaseSchema(FastModel):
    id: UUID


CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
