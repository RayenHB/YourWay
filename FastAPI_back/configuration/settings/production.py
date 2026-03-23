from pydantic_settings import SettingsConfigDict

from FastAPI_back.configuration.settings.app import AppSettings


class ProdAppSettings(AppSettings):
    docs_url: str | None = None
    redoc_url: str | None = None
    openapi_url: str | None = None

    model_config = SettingsConfigDict(
        env_file=('prod.env',)
    )
