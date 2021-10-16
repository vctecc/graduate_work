import os
from logging import config as logging_config
from typing import Any, Dict, Optional

from pydantic import BaseSettings, Field, PostgresDsn, validator

from .logger import LOG_CONFIG

logging_config.dictConfig(LOG_CONFIG)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class DataBaseSettings(BaseSettings):
    host: str = Field("127.0.0.1", env="SUBSCRIPTIONS_DB_HOST")
    port: str = Field('5432', env="SUBSCRIPTIONS_DB_PORT")
    name: str = Field("subscriptions", env="SUBSCRIPTIONS_DB")
    user: str = Field("postgres", env="SUBSCRIPTIONS_DB_USER")
    password: str = Field("password", env="SUBSCRIPTIONS_DB_PASSWORD")

    sqlalchemy_uri: Optional[PostgresDsn] = None

    @validator("sqlalchemy_uri", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v

        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("user"),
            password=values.get("password"),
            host=values.get("host"),
            port=values.get("port"),
            path=f"/{values.get('name') or ''}",
        )


class CacheSettings(BaseSettings):
    host: str = Field("127.0.0.1", env="CACHE_HOST")
    port: int = Field(6379, env="CACHE_PORT")
    expire: int = Field(420, env="CACHE_EXPIRE")
    # backoff_time: int = Field(10, "CACHE_BACKOFF_TIME")


class BackoffSettings(BaseSettings):
    base: float = Field(2, env="BACKOFF_BASE")
    factor: float = Field(1, env="BACKOFF_FACTOR")
    max_value: int = Field(5, env="BACKOFF_MAX_VALUE")


class ProjectSettings(BaseSettings):
    project_name: str = "Subscription API"
    debug: bool = True
    database = DataBaseSettings()
    cache = CacheSettings()
    backoff = BackoffSettings()


settings = ProjectSettings()
