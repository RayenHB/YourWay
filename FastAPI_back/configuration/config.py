from functools import lru_cache
from typing import Dict, Type

from FastAPI_back.configuration.settings.app import AppSettings
from FastAPI_back.configuration.settings.base import AppEnvTypes, BaseAppSettings
from FastAPI_back.configuration.settings.development import DevAppSettings
from FastAPI_back.configuration.settings.production import ProdAppSettings
from FastAPI_back.configuration.settings.test import TestAppSettings

environments: Dict[AppEnvTypes, Type[AppSettings]] = {
    AppEnvTypes.dev: DevAppSettings,
    AppEnvTypes.prod: ProdAppSettings,
    AppEnvTypes.test: TestAppSettings,
}


@lru_cache
def get_app_settings() -> AppSettings:
    app_env = BaseAppSettings().app_env
    config = environments[app_env]
    return config()
