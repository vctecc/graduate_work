from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models import Customer
from src.db.session import get_db
from src.providers import AbstractProvider, get_default_provider


class CustomerService(object):

    def __init__(self, db: Session, provider: AbstractProvider):
        self.db = db
        self.provider = provider

    async def get_customer(self, user_id) -> Customer:
        customer = await self.db.execute(
            select(
                Customer.id, Customer.provider_customer_id
            ).where(
                Customer.user_id == user_id
            )
        )
        customer = customer.first()
        if not customer:
            customer = await self.create_customer(user_id)

        await self.db.flush()
        return customer

    async def create_customer(self, user_id):
        provider_customer = await self.provider.create_customer()
        customer = Customer(
            user_id=user_id,
            provider_customer_id=provider_customer.id,
        )
        self.db.add(customer)
        return customer


def get_customer_service(
        db: Session = Depends(get_db),
        provider: AbstractProvider = Depends(get_default_provider),
):
    return CustomerService(
        db=db,
        provider=provider
    )
