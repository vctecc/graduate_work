from uuid import UUID

import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class BaseSchema(BaseModel):
    id: UUID

    class Config:
        orm_mode = True

    class Meta:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
