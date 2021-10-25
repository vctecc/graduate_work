import pathlib
import logging.config as logging_config
from typing import Optional

from pydantic import BaseSettings, Field, validator


class PaymentsSettings(BaseSettings):
    host: str = Field("localhost", env="PAYMENTS_HOST")
    port: str = Field("8000", env="PAYMENTS_PORT")
    version: str = Field('v1', env="PAYMENTS_API_VERSION")
    url: Optional[str] = None

    @validator("url", pre=True)
    def set_url(cls, v: Optional[str], values: dict) -> str:  # noqa
        return f'http://{values["host"]}:{values["port"]}/{values["version"]}'


class Settings(BaseSettings):
    test: bool = Field(False, env='PAYMENTS_WORKER_TEST')
    subscription_api = Field(default='localhost:8001', env='SUBSCRIPTION_API_URL')
    payments_api = PaymentsSettings()
    stripe_secret_key = Field(
        "sk_test_51JgyKcEZwW9AoJC2MGWJoxsNrzIbA9bDCigTsDfSfJh8vubWxS1tGaDKdIlxLAAk6CJ0aTyd1a1Xoe5cK6PcAdSE00Aycq2uCP",
        env="STRIPE_SECRET_KEY")
    broker_url = Field("pyamqp://guest:guest@localhost//", env="BROKER_URL")


settings = Settings()

LOGGER_CONFIG = pathlib.Path(__file__).parent / 'logging.conf'
LOGGER_NAME = 'order_service'
logging_config.fileConfig(LOGGER_CONFIG)
