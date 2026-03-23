from pydantic_settings import SettingsConfigDict

from FastAPI_back.configuration.settings.app import AppSettings


class ProdAppSettings(AppSettings):
    model_config = SettingsConfigDict(
        env_file=('prod.env',)
    )
