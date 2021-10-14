import datetime
import uuid
from functools import partial
from typing import Any

from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.sql import func


@as_declarative()
class Base:
    id: Any
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


@as_declarative()
class TimeStampBase:
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    modified = Column(DateTime, onupdate=func.now())
    created = Column(DateTime, default=datetime.datetime.utcnow)
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


RequiredColumn = partial(Column, nullable=False)
