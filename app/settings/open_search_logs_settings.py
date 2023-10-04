from typing import Any, Dict, Optional, Union

from opensearch_logger.handlers import RotateFrequency
from pydantic_settings import BaseSettings, SettingsConfigDict


class OpenSearchLogsSettings(BaseSettings):
    """
    Here goes any logging specific settings.
    """

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Logger settings
    index_name: str = "my-app-logs"
    index_rotate: Union[RotateFrequency, str] = RotateFrequency.DAILY
    index_date_format: str = "%Y.%m.%d"
    index_name_sep: str = "-"
    buffer_size: int = 1000
    flush_frequency: float = 1.0
    extra_fields: Optional[Dict[str, Any]] = None
    raise_on_index_exc: bool = True

    # OpenSearch settings
    open_search_host: Optional[str] = None  # The OpenSearch domain endpoint starting with https://
    region: Optional[str] = None  # AWS Region
    use_ssl: bool = True
    verify_certs: bool = True
    ssl_assert_hostname: bool = True
    ssl_show_warn: bool = True


os_logs_settings = OpenSearchLogsSettings()
