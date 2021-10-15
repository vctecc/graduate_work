#! /usr/bin/env python3

import logging
from app.db.session import SessionLocal
from app.models.product import Product


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_db() -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    product = {
        "id": "a49b436a-d0b3-4e3e-84e5-ac9204a330a5",
        "name": "Rick and Morty",
        "description": "Mega movie",
        "price": 200,
        "currency_code": "RUB",
        "period": 100500,
        "is_active": True
    }
    db_obj = Product(**product)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)


def main() -> None:
    logger.info("Creating initial data")
    init_db()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
