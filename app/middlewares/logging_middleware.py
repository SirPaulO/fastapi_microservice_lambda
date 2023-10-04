import dataclasses
import logging
import math
import time
import typing
from typing import ClassVar

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, DispatchFunction, RequestResponseEndpoint
from starlette.types import ASGIApp, Receive

EMPTY_VALUE = ""
PASS_ROUTES = [
    "/openapi.json",
    "/docs",
    "/healthcheck",
]


@dataclasses.dataclass
class ReceiveProxy:
    """Proxy to starlette.types.Receive.__call__ with caching first receive call.
    https://github.com/tiangolo/fastapi/issues/394#issuecomment-994665859
    """

    def __init__(self, receive: Receive, cached_body: bytes):
        self.receive = receive
        self.cached_body = cached_body
        self._is_first_call: ClassVar[bool] = True  # type: ignore

    async def __call__(self) -> typing.Any:
        # First call will be for getting request body => returns cached result
        if self._is_first_call:
            self._is_first_call = False
            return {
                "type": "http.request",
                "body": self.cached_body,
                "more_body": False,
            }

        return await self.receive()


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware that logs Request and Response

    Based on https://github.com/mostepunk/fastapi-json-log
    """

    logger = logging.getLogger("app." + __name__)

    def __init__(
        self,
        app: ASGIApp,
        dispatch: typing.Optional[DispatchFunction] = None,
        logger_name: typing.Optional[str] = None,
    ):
        super().__init__(app, dispatch)
        if logger_name:
            self.logger = logging.getLogger(logger_name)

    @staticmethod
    async def get_protocol(request: Request) -> str:
        protocol = str(request.scope.get("type", ""))
        http_version = str(request.scope.get("http_version", ""))
        if protocol.lower() == "http" and http_version:
            return f"{protocol.upper()}/{http_version}"
        return EMPTY_VALUE

    @staticmethod
    async def get_request_body(request: Request) -> bytes:
        body = await request.body()

        request._receive = ReceiveProxy(receive=request.receive, cached_body=body)
        return body

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if request.url.path in PASS_ROUTES:
            return await call_next(request)

        start_time = time.time()
        request_body = await self.get_request_body(request)
        server: tuple = request.get("server", ("localhost", 0000))
        request_headers: dict = dict(request.headers.items())

        self.logger.info(
            "Request",
            extra={
                "start_time": start_time,
                "request_uri": str(request.url),
                "request_referer": request_headers.get("referer", EMPTY_VALUE),
                "request_method": request.method,
                "request_path": request.url.path,
                "request_host": f"{server[0]}:{server[1]}",
                "request_size": int(request_headers.get("content-length", 0)),
                "request_content_type": request_headers.get("content-type", EMPTY_VALUE),
                "request_headers": request_headers,
                "request_body": str(request_body),
            },
        )

        # Response Side
        try:
            response = await call_next(request)
        except Exception as ex:
            logging.error(f"Exception: {ex}", exc_info=ex)
            raise

        response_headers = dict(response.headers.items())
        response_body = b""

        async for chunk in response.body_iterator:
            response_body += chunk

        response = Response(
            content=response_body,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type,
        )

        duration: int = math.ceil((time.time() - start_time) * 1000)

        self.logger.info(
            "Response",
            extra={
                "response_status_code": response.status_code,
                "response_size": int(response_headers.get("content-length", 0)),
                "response_headers": response_headers,
                "response_body": str(response_body),
                "duration": duration,
            },
        )

        return response
