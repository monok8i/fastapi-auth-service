"""Exceptions handlers for the API."""

from fastapi import Request
from fastapi.responses import JSONResponse


async def invalid_token_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    """Handle InvalidTokenException."""

    return JSONResponse(
        status_code=401,
        content={"detail": "Invalid token"},
    )


async def unauthorized_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    """Handle UnauthorizedException."""

    return JSONResponse(
        status_code=401,
        content={"detail": "Unauthorized"},
    )


async def no_code_provided_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    """Handle NoCodeProvidedException."""

    return JSONResponse(
        status_code=400,
        content={"detail": "No code provided"},
    )


async def token_expired_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    """Handle TokenExpiredException."""

    return JSONResponse(
        status_code=401,
        content={"detail": "Token has expired"},
    )
