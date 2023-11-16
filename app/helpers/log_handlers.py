from logging import Handler, StreamHandler

import boto3
from opensearch_logger import OpenSearchHandler
from opensearchpy import RequestsHttpConnection
from requests_aws4auth import AWS4Auth
from settings.open_search_logs_settings import os_logs_settings

open_search_handler: Handler

if os_logs_settings.open_search_host:
    creds = boto3.Session().get_credentials()
    open_search_handler = OpenSearchHandler(
        http_auth=AWS4Auth(region=os_logs_settings.region, service="es", refreshable_credentials=creds),
        connection_class=RequestsHttpConnection,
        hosts=[os_logs_settings.open_search_host],
        index_name=os_logs_settings.index_name,
        index_rotate=os_logs_settings.index_rotate,
        index_date_format=os_logs_settings.index_date_format,
        index_name_sep=os_logs_settings.index_name_sep,
        buffer_size=os_logs_settings.buffer_size,
        flush_frequency=os_logs_settings.flush_frequency,
        extra_fields=os_logs_settings.extra_fields,
        raise_on_index_exc=os_logs_settings.raise_on_index_exc,
    )
else:
    open_search_handler = StreamHandler()
