from logging import config as logging_config
from typing import Optional, Dict, Any, Union

from pydantic import Field, BaseSettings, PostgresDsn, validator

from .logger import LOGGING

logging_config.dictConfig(LOGGING)


class PostgresDsnWithAsync(PostgresDsn):
    allowed_schemes = {'postgres', 'postgresql', 'postgresql+asyncpg'}


class DataBaseSettings(BaseSettings):
    host: str = Field("127.0.0.1", env="POSTGRES_HOST")
    port: str = Field('5432', env="POSTGRES_PORT")
    name: str = Field("payments", env="PAYMENTS_DB")
    user: str = Field("postgres", env="POSTGRES_USER")
    password: str = Field("password", env="POSTGRES_PASSWORD")

    sqlalchemy_uri: Optional[str] = None

    @validator("sqlalchemy_uri", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        if isinstance(v, str):
            return v

        return PostgresDsnWithAsync.build(
            scheme="postgresql+asyncpg",
            user=values.get("user"),
            password=values.get("password"),
            host=values.get("host"),
            port=values.get("port"),
            path=f"/{values.get('name') or ''}",
        )

class SubscriptionsSettings(BaseSettings):
    host: str = Field("127.0.0.1", env="SUBSCRIPTION_HOST")
    port: str = Field('8001', env="SUBSCRIPTION_PORT")
    url: Optional[str] = None

    @validator("url", pre=True)
    def set_url(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        return f'{values["host"]}:{values["port"]}'


class ProjectSettings(BaseSettings):
    project_name: str = "Payments API"
    debug: bool = Field(True, env="PAYMENTS_DEBUG")
    stripe_secret_key = Field("", env="STRIPE_SECRET_KEY")
    jwt_secret_key = Field("", env="JWT_SECRET_KEY")
    jwt_algorithm = Field("HS256", env="JWT_ALGORITHM")
    database = DataBaseSettings()
    subscriptions = SubscriptionsSettings()


settings = ProjectSettings()
