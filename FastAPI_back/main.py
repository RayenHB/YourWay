import sys
from os.path import abspath, dirname
from pathlib import Path
from typing import Any, Dict, List

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

# Add parent directory to sys.path
parent_path = dirname(dirname(abspath(__file__)))
sys.path.append(parent_path)

from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

from FastAPI_back.api import api_router
from FastAPI_back.configuration.config import get_app_settings
from FastAPI_back.db.events import *
from FastAPI_back.dependencies.repository import get_session_v2
from FastAPI_back.resources.vars import excluded_routes
from FastAPI_back.utils.error_handlers import (
    custom_base_errors_handler,
    pydantic_validation_errors_handler,
    python_base_error_handler,
)
from FastAPI_back.utils.errors import BaseError, NotFoundError
from FastAPI_back.utils.events import handle_server_startup_event







def get_application() -> FastAPI:
    settings = get_app_settings()
    settings.configure_logging()
    application = FastAPI(**settings.fastapi_kwargs)

    static_dir = Path(__file__).resolve().parent / "PhonesImages"
    application.mount(
        "/static",
        StaticFiles(directory=str(static_dir)),
        name="static",
    )

    # CORS Middleware
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # Extend FastAPI default error handlers
    application.exception_handler(RequestValidationError)(pydantic_validation_errors_handler)
    application.exception_handler(BaseError)(custom_base_errors_handler)
    application.exception_handler(ValidationError)(pydantic_validation_errors_handler)
    application.exception_handler(Exception)(python_base_error_handler)
    application.add_event_handler("startup", handle_server_startup_event)
    application.include_router(api_router, prefix=settings.api_prefix)
    return application


app = get_application()


