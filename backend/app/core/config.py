from pydantic_settings import BaseSettings, SettingsConfigDict

import secrets


class Settings(BaseSettings):
    # common settings
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # one day

    # service settings
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./sql_app.db"

    model_config = SettingsConfigDict(
        case_sensitive=True, env_file="../app.env", env_file_encoding="utf-8"
    )


settings = Settings()
