from sqlalchemy import Column, String, Integer, Boolean

from app.db import TimeStampBase, RequiredColumn


class Product(TimeStampBase):
    name = RequiredColumn(String(255))
    description = Column(String(255))
    period = RequiredColumn(Integer)
    price = RequiredColumn(Integer)
    currency_code = Column(String(3), default='RUB')
    is_active = Column(Boolean, default=True)
