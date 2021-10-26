#! /usr/bin/env python3
import logging
import asyncio
from datetime import datetime, timedelta

from sqlalchemy import delete

from app.db.session import async_session
from app.models.product import Product
from app.models.subscription import Subscription

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

START_DATE = datetime.strptime("2021-10-15", "%Y-%m-%d")
PRODUCTS = (
    {
        "id": "a49b436a-d0b3-4e3e-84e5-ac9204a330a5",
        "name": "Rick and Morty",
        "description": "Adult animated science fiction sitcom.",
        "price": 20000,
        "currency_code": "RUB",
        "period": 30,
        "is_active": True
    },
    {
        "id": "a49b436a-d0b3-4e3e-84e5-ac9204a33666",
        "name": "Goose",
        "description": "Most important film.",
        "price": 20000,
        "currency_code": "RUB",
        "period": 30,
        "is_active": False
    },
)
SUBSCRIPTIONS = (
    {
        "id": "429b436a-d0b3-4e3e-84e5-ac9204a33042",
        "user_id": "a49b436a-d0b3-4e3e-84e5-ac9204a33042",
        "product_id": "a49b436a-d0b3-4e3e-84e5-ac9204a330a5",
        "state": "active",
        "start_date": START_DATE,
        "end_date": START_DATE + timedelta(days=30),
    },
    {
        "id": "429b436a-d0b3-4e3e-84e5-789204a33042",
        "user_id": "a49b436a-d0b3-4e3e-84e5-ac9204a33042",
        "product_id": "a49b436a-d0b3-4e3e-84e5-ac9204a330a5",
        "state": "active",
        "start_date": START_DATE,
        "end_date": START_DATE + timedelta(days=30),
    },
    {
        "id": "429b436a-d042-4e3e-84e5-789204a33042",
        "user_id": "a49b436a-d0b3-4e3e-84e5-ac9204a33042",
        "product_id": "a49b436a-d0b3-4e3e-84e5-ac9204a330a5",
        "state": "active",
        "start_date": START_DATE,
        "end_date": START_DATE + timedelta(days=30),
    },
    {
        "id": "429b436a-d042-4e3e-1488-789204a33042",
        "user_id": "a49b436a-d0b3-4e3e-84e5-ac9204a33042",
        "product_id": "a49b436a-d0b3-4e3e-84e5-ac9204a330a5",
        "state": "active",
        "start_date": START_DATE - timedelta(days=30),
        "end_date": START_DATE,
    },
    {
        "id": "429b436a-d042-4e3e-2866-789204a33042",
        "user_id": "a49b436a-d0b3-4e3e-84e5-ac9204a33042",
        "product_id": "a49b436a-d0b3-4e3e-84e5-ac9204a330a5",
        "state": "active",
        "start_date": START_DATE - timedelta(days=30),
        "end_date": START_DATE,
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
        for table in (Subscription, Product):
            await session.execute(delete(table))
        await session.commit()


async def init_db():
    await db_add(Product, PRODUCTS)
    await db_add(Subscription, SUBSCRIPTIONS)


async def async_main() -> None:
    logger.info("Cleaning old data")
    await clean_db()
    logger.info("Creating initial data")
    await init_db()
    logger.info("Initial data created")


if __name__ == "__main__":
    asyncio.run(async_main())
