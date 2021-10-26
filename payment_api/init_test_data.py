#! /usr/bin/env python3
import logging
import asyncio

from sqlalchemy import delete

from src.db.session import async_session
from src.models.payments import Payment
from src.models.customer import Customer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CUSTOMERS = (
    {
        "id": 1,
        "user_id": "a49b436a-d0b3-4e3e-84e5-ac9204a33042",
        "provider_customer_id": "cus_KSkOhnNYigh8Mc",
    },
)
PAYMENTS = (
    {
        "id": 2,
        "invoice_id": "pi_3JnrIvEZwW9AoJC20hPPg3ua",
        "product_id": "a49b436a-d0b3-4e3e-84e5-ac9204a330a5",
        "customer_id": 1,
        "status": 'paid'
    },
)


async def db_add(model, objs: tuple):
    async with async_session() as session:
        for obj in objs:
            db_obj = model(**obj)
            session.add(db_obj)
        await session.commit()


async def clean_db():
    async with async_session() as session:
        for table in (Payment, Customer):
            await session.execute(delete(table))
        await session.commit()


async def init_db():
    await db_add(Customer, CUSTOMERS)
    await db_add(Payment, PAYMENTS)


async def async_main() -> None:
    logger.info("Cleaning old data")
    await clean_db()
    logger.info("Creating initial data")
    await init_db()
    logger.info("Initial data created")


if __name__ == "__main__":
    asyncio.run(async_main())
