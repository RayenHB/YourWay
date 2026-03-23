import logging

from pydantic_settings import SettingsConfigDict

from FastAPI_back.configuration.settings.app import AppSettings


class DevAppSettings(AppSettings):
    debug: bool = True

    title: str = "Xtend Recruit API Documentation  DEV-MODE"

    logging_level: int = logging.INFO

    model_config = SettingsConfigDict(
        env_file=('.env',)
    )
