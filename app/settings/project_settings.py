from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class ProjectSettings(BaseSettings):
    """
    Here goes any project specific settings.
    """

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DEBUG: Optional[bool] = True
    Environment: Optional[str] = "local"


project_settings = ProjectSettings()
