from pydantic_settings import BaseSettings, SettingsConfigDict


class ProjectSettings(BaseSettings):
    """
    Here goes any project specific settings.
    """

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    ExampleSettingStr: str


project_settings = ProjectSettings()
