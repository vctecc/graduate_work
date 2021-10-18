#! /usr/bin/env python3
import logging
from datetime import datetime, timedelta

from app.db.session import SessionLocal
from app.models.product import Product
from app.models.subscription import Subscription

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

db = SessionLocal()


def db_add(model, objs: tuple):
    for obj in objs:
        db_obj = model(**obj)
        db.add(db_obj)
    db.commit()


def clean_db():
    for model in (Subscription, Product):
        db.query(model).delete()
    db.commit()


def init_db():
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)
    products = (
        {
            "id": "a49b436a-d0b3-4e3e-84e5-ac9204a330a5",
            "name": "Rick and Morty",
            "description": "Adult animated science fiction sitcom.",
            "price": 20000,
            "currency_code": "RUB",
            "period": 30,
            "is_active": True
        },
    )
    db_add(Product, products)

    start_date = datetime.strptime("2021-10-15", "%Y-%m-%d")
    subscriptions = (
        {
            "id": "429b436a-d0b3-4e3e-84e5-ac9204a33042",
            "user_id": "a49b436a-d0b3-4e3e-84e5-ac9204a33042",
            "product_id": "a49b436a-d0b3-4e3e-84e5-ac9204a330a5",
            "state": "active",
            "start_date": start_date,
            "end_date": start_date + timedelta(days=30),
        },
        {
            "id": "429b436a-d0b3-4e3e-84e5-789204a33042",
            "user_id": "a49b436a-d0b3-4e3e-84e5-ac9204a33042",
            "product_id": "a49b436a-d0b3-4e3e-84e5-ac9204a330a5",
            "state": "active",
            "start_date": start_date,
            "end_date": start_date + timedelta(days=30),
        },
        {
            "id": "429b436a-d042-4e3e-84e5-789204a33042",
            "user_id": "a49b436a-d0b3-4e3e-84e5-ac9204a33042",
            "product_id": "a49b436a-d0b3-4e3e-84e5-ac9204a330a5",
            "state": "active",
            "start_date": start_date,
            "end_date": start_date + timedelta(days=30),
        },
    )

    db_add(Subscription, subscriptions)


def main() -> None:
    logger.info("Cleaning old data")
    clean_db()
    logger.info("Creating initial data")
    init_db()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
