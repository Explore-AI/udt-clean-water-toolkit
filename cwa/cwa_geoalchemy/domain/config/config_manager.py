from pydantic_settings import BaseSettings, SettingsConfigDict, EnvSettingsSource
from pydantic import Field


class Settings(BaseSettings):
    # gis env vars 
    POSTGIS_DB_NAME: str = Field(alias="POSTGIS_DB_NAME__ENV_VAR")
    POSTGIS_DB_USER: str = Field(alias="POSTGIS_DB_USER__ENV_VAR")
    POSTGIS_DEFAULT_DB_HOST: str = Field(
        alias="POSTGIS_DEFAULT_DB_HOST__ENV_VAR"
    )
    POSTGIS_DEFAULT_DB_PASSWORD: str = Field(
        alias="POSTGIS_DEFAULT_DB_PASSWORD__ENV_VAR"
    )
    POSTGIS_DEFAULT_PORT: int = Field(alias="POSTGIS_DEFAULT_PORT__ENV_VAR")
    # neo4j env vars
    NEO4J_USER: str = Field(alias="NEO4J_USER__ENV_VAR")
    NEO4J_PASSWORD: str = Field(alias="NEO4J_PASSWORD__ENV_VAR")
    

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True
    )
