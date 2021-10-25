import pathlib
import logging.config as logging_config
from typing import Optional

from pydantic import BaseSettings, Field, validator


class SubscriptionSettings(BaseSettings):
    host: str = Field("localhost", env="SUBSCRIPTION_HOST")
    port: str = Field("8001", env="SUBSCRIPTION_PORT")
    version: str = Field('api/v1', env="SUBSCRIPTION_API_VERSION")
    url: Optional[str] = None

    @validator("url", pre=True)
    def set_url(cls, v: Optional[str], values: dict) -> str:  # noqa
        return f'http://{values["host"]}:{values["port"]}/{values["version"]}'


class PaymentsSettings(BaseSettings):
    host: str = Field("localhost", env="PAYMENTS_HOST")
    port: str = Field("8000", env="PAYMENTS_PORT")
    version: str = Field('v1', env="PAYMENTS_API_VERSION")
    url: Optional[str] = None

    @validator("url", pre=True)
    def set_url(cls, v: Optional[str], values: dict) -> str:  # noqa
        return f'http://{values["host"]}:{values["port"]}/{values["version"]}'


class Settings(BaseSettings):
    test: bool = Field(False, env='SUBSCRIPTION_WORKER_TEST')
    payments_api = PaymentsSettings()
    subscription_api = SubscriptionSettings()
    broker_url = Field("pyamqp://guest:guest@localhost//", env="BROKER_URL")


settings = Settings()

LOGGER_CONFIG = pathlib.Path(__file__).parent / 'logging.conf'
LOGGER_NAME = 'order_service'
logging_config.fileConfig(LOGGER_CONFIG)
