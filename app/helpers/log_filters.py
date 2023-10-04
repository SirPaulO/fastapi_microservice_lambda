import logging
from typing import Dict, Optional

from starlette_context import context
from starlette_context.errors import ContextDoesNotExistError


class LoggerStarletteContextExtraDataFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        request_id: Optional[str] = None
        extra_data: Dict = {}

        try:
            request_id = context.data.get("X-Request-ID")
            extra_data = context.data.get("logger_extra_data", {})
        except ContextDoesNotExistError:
            pass

        if request_id:
            setattr(record, "X-Request-ID", request_id)

        for k in extra_data:
            setattr(record, k, extra_data[k])

        return True
