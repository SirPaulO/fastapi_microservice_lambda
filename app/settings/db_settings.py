from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class DBSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # ===== DB
    DBProtocol: Optional[str] = None
    DBUser: Optional[str] = None
    DBPassword: Optional[str] = None
    DBHost: Optional[str] = None
    DBName: Optional[str] = None
    DBConnectionString: Optional[str] = None


db_settings = DBSettings()
