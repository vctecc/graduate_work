import os
from logging import config as logging_config

from .logger import LOGGING

logging_config.dictConfig(LOGGING)

PROJECT_NAME = os.getenv("PROJECT_NAME", "Payment API")
DEBUG = bool(os.getenv("DEBUG")) or False

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", 5432)
POSTGRES_DB_NAME = os.getenv("POSTGRES_DB_NAME", "postgres")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")

SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@" \
                          f"{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB_NAME}"

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")