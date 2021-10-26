import os
from logging import config as logging_config
from typing import Any, Dict, Optional

from pydantic import BaseSettings, Field, PostgresDsn, validator

from .logger import LOG_CONFIG

logging_config.dictConfig(LOG_CONFIG)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class PostgresDsnAsync(PostgresDsn):
    allowed_schemes = {'postgres', 'postgresql', 'postgresql+asyncpg'}


class DataBaseSettings(BaseSettings):
    host: str = Field("127.0.0.1", env="SUBSCRIPTIONS_DB_HOST")
    port: str = Field('5432', env="SUBSCRIPTIONS_DB_PORT")
    name: str = Field("subscriptions", env="SUBSCRIPTIONS_DB")
    user: str = Field("postgres", env="SUBSCRIPTIONS_DB_USER")
    password: str = Field("password", env="SUBSCRIPTIONS_DB_PASSWORD")

    sqlalchemy_uri: Optional[PostgresDsnAsync] = None

    @validator("sqlalchemy_uri", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v

        return PostgresDsnAsync.build(
            scheme='postgresql+asyncpg',
            user=values.get("user"),
            password=values.get("password"),
            host=values.get("host"),
            port=values.get("port"),
            path=f"/{values.get('name') or ''}",
        )


class CacheSettings(BaseSettings):
    host: str = Field("127.0.0.1", env="REDIS_HOST")
    port: int = Field(6379, env="REDIS_PORT")
    expire: int = Field(420, env="CACHE_EXPIRE")


class BackoffSettings(BaseSettings):
    base: float = Field(2, env="BACKOFF_BASE")
    factor: float = Field(1, env="BACKOFF_FACTOR")
    max_time: int = Field(10, env="BACKOFF_MAX_TIME")
    max_value: int = Field(5, env="BACKOFF_MAX_VALUE")


class AuthSettings(BaseSettings):
    algorithm: str = Field("HS256", env="AUTH_ALGORITHM")  # FIXME use RS256
    secret_key: Optional[str] = "super-secret"  # FIXME get key from auth service


class PaymentsAPISettings(BaseSettings):
    host: str = Field("localhost", env="PAYMENTS_HOST")
    port: str = Field('8000', env="PAYMENTS_PORT")
    suffix: str = Field("api/v1/payments/cancel/")
    url: Optional[str] = None

    @validator("url", pre=True)
    def set_url(cls, v: Optional[str], values: Dict[str, Any]) -> str:  # noqa
        return f'http://{values["host"]}:{values["port"]}/{values["suffix"]}'


class ProjectSettings(BaseSettings):
    project_name: str = "Subscription API"
    debug: bool = True
    database = DataBaseSettings()
    cache = CacheSettings()
    backoff = BackoffSettings()
    auth = AuthSettings()


settings = ProjectSettings()
