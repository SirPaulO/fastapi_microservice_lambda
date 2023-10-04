import logging

from api.external_api import api_router as api_router_external
from api.internal_api import api_router as api_router_internal
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi_exceptionshandler import APIExceptionHandler, APIExceptionMiddleware
from fastapi_versioning import VersionedFastAPI
from helpers.log_filters import LoggerStarletteContextExtraDataFilter
from helpers.log_handlers import open_search_handler
from middlewares.logging_middleware import LoggingMiddleware
from pydantic import ValidationError
from starlette.middleware.cors import CORSMiddleware
from starlette_context import plugins
from starlette_context.middleware import RawContextMiddleware

app = FastAPI(
    title="MSExample",
    description="Example Microservice running on FastAPI",
)

# ==== Include external routes
app.include_router(api_router_external)

# ==== Version
app = VersionedFastAPI(app)

# ==== Include internal routes
app.include_router(api_router_internal, prefix="/internal")

# ==== Logging
logger = logging.getLogger("app")
logger.addHandler(logging.StreamHandler())
logger.addHandler(open_search_handler)
open_search_handler.addFilter(LoggerStarletteContextExtraDataFilter())

# ==== Middlewares
app.add_middleware(LoggingMiddleware, logger_name="app.requests")
app.add_middleware(
    APIExceptionMiddleware,
    capture_unhandled=True,
    log_error=True,
    logger_name="app.exceptions",
)
app.add_middleware(RawContextMiddleware, plugins=(plugins.RequestIdPlugin(),))
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==== Exception handlers
app.add_exception_handler(RequestValidationError, APIExceptionHandler.unhandled)
app.add_exception_handler(ValidationError, APIExceptionHandler.unhandled)
