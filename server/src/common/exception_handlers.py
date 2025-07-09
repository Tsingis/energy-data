from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from slowapi.errors import RateLimitExceeded
from .setup_logger import setup_logger

logger = setup_logger()


def http_exception_handler(_: Request, exc: StarletteHTTPException):
    logger.exception(f"HTTP Exception: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": "An error occurred"},
    )


def fastapi_http_exception_handler(_: Request, exc: HTTPException):
    logger.exception(f"HTTP Exception: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": "An error occurred"},
    )


def validation_exception_handler(_: Request, exc: RequestValidationError):
    logger.exception(f"Validation Error: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={"error": "Invalid request"},
    )


def general_exception_handler(_: Request, exc: Exception):
    logger.exception(f"Unhandled Exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"},
    )


def ratelimit_exception_handler(_: Request, exc: RateLimitExceeded):
    logger.exception("Rate limit exceeded", exc_info=exc)
    return JSONResponse(
        status_code=429,
        content={"message": "Rate limit exceeded. Try again later."},
    )
