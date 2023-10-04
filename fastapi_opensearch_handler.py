import logging
from collections.abc import MutableMapping
from typing import Dict, Any, Optional, Callable

from opensearch_logger import OpenSearchHandler
from starlette_context import context
from starlette_context.errors import ContextDoesNotExistError


class FastAPIOpenSearchHandler(OpenSearchHandler):
    doc_filter_callback: Optional[Callable] = None

    @staticmethod
    def get_request_id() -> Optional[str]:
        try:
            from starlette_context import context
            return context.data.get("X-Request-ID")
        except Exception:
            return None

    def _convert_log_record_to_doc(self, record: logging.LogRecord) -> Dict[str, Any]:
        doc = super()._convert_log_record_to_doc(record)

        if rid := self.get_request_id() and "X-Request-ID" not in doc:
            doc["X-Request-ID"] = rid

        if self.doc_filter_callback:
            doc = self.doc_filter_callback(doc)

        return doc


class StarletteContextLoggerExtraDataAdapter(MutableMapping):
    EXTRA_DATA_KEY_NAME = "logger_extra_data"

    def _set_context(self) -> None:
        if self.EXTRA_DATA_KEY_NAME in context.data:
            return
        context.data[self.EXTRA_DATA_KEY_NAME] = {}
        if self.copy_request_id:
            context.data[self.EXTRA_DATA_KEY_NAME]["X-Request-ID"] = context.data.get("X-Request-ID")

    def __init__(self, key_name: str = EXTRA_DATA_KEY_NAME, copy_request_id: bool = True):
        self.EXTRA_DATA_KEY_NAME = key_name
        self.copy_request_id = copy_request_id

    def __getitem__(self, item: Any) -> Any:
        return context.data[self.EXTRA_DATA_KEY_NAME][item]

    def __delitem__(self, item: Any) -> None:
        del context.data[self.EXTRA_DATA_KEY_NAME][item]

    def __len__(self) -> int:
        return len(context.data[self.EXTRA_DATA_KEY_NAME])

    def __setitem__(self, item: Any, value: Any) -> None:
        self._set_context()
        context.data[self.EXTRA_DATA_KEY_NAME][item] = value

    def __iter__(self):
        self._set_context()
        return context.data[self.EXTRA_DATA_KEY_NAME].__iter__()


class StarletteContextLoggerExtraDataFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        extra_data = dict(StarletteContextLoggerExtraDataAdapter())
        for k in extra_data:
            setattr(record, k, extra_data[k])
        return True
