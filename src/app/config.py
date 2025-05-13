import os

from typing import Final

from pydantic_settings import BaseSettings, SettingsConfigDict


path_env = os.path.join(os.path.dirname(__file__), ".env")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        validate_default=False,
        env_file=path_env,
        extra="ignore",
    )

    # APP
    APP_NAME: str
    APP_PORT: int
    APP_HOST: str
    APP_VERSION: str
    APP_DEBUG: bool
    APP_ENV: str = "local"

    # DATABASE
    POSTGRE_HOST: str
    POSTGRE_PORT: int
    POSTGRE_USER: str
    POSTGRE_PASSWORD: str
    POSTGRE_DB: str

    # REDIS
    REDIS_HOST: str
    REDIS_PORT: int

    WHITELIST_CLIENT_IDS: str


settings: Final[Settings] = Settings()
