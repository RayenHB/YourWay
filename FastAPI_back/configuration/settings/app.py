import logging
import sys
from typing import Any, Dict, List, Tuple

from loguru import logger
from pydantic import PostgresDsn, SecretStr
from pydantic_settings import SettingsConfigDict
from dotenv import load_dotenv
from FastAPI_back.configuration.logging_handler import InterceptHandler
from FastAPI_back.configuration.settings.base import BaseAppSettings

load_dotenv()


class AppSettings(BaseAppSettings):
    debug: bool = False
    docs_url: str = "/docs"
    openapi_prefix: str = ""
    openapi_url: str = "/openapi.json"
    redoc_url: str = "/redoc"
    title: str = "Smarty Car Simulator API Documentation"
    version: str = "0.1.0"

    database_url: PostgresDsn
    max_connection_count: int = 10
    min_connection_count: int = 10

    secret_key: SecretStr

    api_prefix: str = "/api"

    jwt_token_prefix: str = "Token"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60  # Access token expires in 30 minutes
    refresh_token_expire_days: int = 7     
    @property
    def jwt_config(self) -> Dict[str, Any]:
        return {
            "secret_key": self.secret_key.get_secret_value(),
            "algorithm": self.jwt_algorithm,
            "access_token_expire_minutes": self.access_token_expire_minutes,
            "refresh_token_expire_days": self.refresh_token_expire_days,
            "audience": self.jwt_audience,
            "issuer": self.jwt_issuer,
        }

    allowed_hosts: List[str] = ["*"]

    logging_level: int = logging.INFO
    loggers: Tuple[str, str] = ("uvicorn.asgi", "uvicorn.access")


    model_config = SettingsConfigDict(env_file=('.env',))

    @property
    def fastapi_kwargs(self) -> Dict[str, Any]:
        return {
            "debug": self.debug,
            "docs_url": self.docs_url,
            "openapi_prefix": self.openapi_prefix,
            "openapi_url": self.openapi_url,
            "redoc_url": self.redoc_url,
            "title": self.title,
            "version": self.version,
        }

    def configure_logging(self) -> None:
        logging.getLogger().handlers = [InterceptHandler()]
        for logger_name in self.loggers:
            logging_logger = logging.getLogger(logger_name)
            logging_logger.handlers = [InterceptHandler(level=self.logging_level)]

        logger.configure(handlers=[{"sink": sys.stderr, "level": self.logging_level}])
    
