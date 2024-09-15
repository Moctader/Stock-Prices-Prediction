from typing import Optional
from pydantic import ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_ECHO: bool = False
    DATABASE_URL: Optional[str] = None

    PGADMIN_DEFAULT_EMAIL: str
    PGADMIN_DEFAULT_PASSWORD: str
    PGADMIN_PORT: int
    API_KEY: str
    LOG_LEVEL: str
    FASTAPI_PORT: int
    GRPC_PORT: int
    PROJECT_NAME: str

    LOGGER_CONSOLE: bool
    LOGGER_GRAYLOG: bool
    LOGGER_GRAYLOG_HOST: str
    LOGGER_GRAYLOG_PORT: int
    DEBUG: bool = False

    VERSION: str = "0.1.0"
    DESCRIPTION: str = "API description"
    DOCS_URL: str = "/docs"
    REDOCS_URL: str = "/redoc"
    OPENAPI_URL: str = "/openapi.json"
    API_PREFIX: str = "/api/v1"

    @field_validator("DATABASE_URL", mode="before")
    def assemble_db_connection(cls, v: Optional[str], values: ValidationInfo) -> str:
        if isinstance(v, str):
            return v

        return "postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}".format(
            user=values.data["POSTGRES_USER"],
            password=values.data["POSTGRES_PASSWORD"],
            host=values.data["POSTGRES_HOST"],
            port=values.data["POSTGRES_PORT"],
            db=values.data["POSTGRES_DB"],
        )

    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env")


settings = Settings()
