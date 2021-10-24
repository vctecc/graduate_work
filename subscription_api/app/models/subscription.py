import enum

from sqlalchemy import Column, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db import RequiredColumn, TimeStampBase


class SubscriptionState(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    CANCELLED = "cancelled"


class Subscription(TimeStampBase):
    user_id = RequiredColumn(UUID(as_uuid=True))
    product_id = Column(UUID, ForeignKey("product.id"))
    product = relationship("Product", back_populates="subscriptions")
    state = Column(Enum(SubscriptionState), default=SubscriptionState.ACTIVE)
    start_date = RequiredColumn(DateTime)
    end_date = RequiredColumn(DateTime)
