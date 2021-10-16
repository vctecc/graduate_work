from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# FIXME use async lib
# TODO add backoff
engine = create_engine(settings.database.sqlalchemy_uri, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
