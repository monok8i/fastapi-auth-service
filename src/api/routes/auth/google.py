"""Google authentication endpoints."""

from fastapi import APIRouter, Request, Response, status
from fastapi.responses import JSONResponse, RedirectResponse

from src.api.dependencies import (
    CSRFStorageRepositoryDependency,
    OICGoogleServiceDependency,
)
from src.api.schemas import Token as TokenResponse
from src.core.security.secrets import generate_secret

router = APIRouter(prefix="/google")


@router.get("/", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
async def google(
    service: OICGoogleServiceDependency,
    csrf_storage: CSRFStorageRepositoryDependency,
) -> RedirectResponse:
    """Authenticate user by Google."""

    csrf_token = generate_secret(64)
    nonce = generate_secret(64)
    await csrf_storage.create(csrf_token, nonce, provider="google")

    return RedirectResponse(
        url=service.oauth_provider.get_authorization_url(
            csrf_token=csrf_token, nonce=nonce
        )
    )


@router.get(
    "/callback",
    status_code=status.HTTP_200_OK,
    response_model=TokenResponse,
)
async def google_callback(
    code: str,
    state: str,
    request: Request,
    response: Response,
    service: OICGoogleServiceDependency,
    csrf_storage: CSRFStorageRepositoryDependency,
):
    """Handle Google auth callback."""

    ip_address = request.client.host if request.client else "unknown"

    csrf_session = await csrf_storage.get(state)
    if not csrf_session:
        return JSONResponse(
            content={"detail": "Invalid or expired CSRF token"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    if state != csrf_session.token:
        return JSONResponse(
            content={"detail": "CSRF token mismatch"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    token = await service.login(code=code, ip_address=ip_address)

    response.set_cookie(
        "refresh_token",
        token.refresh_token,
        httponly=True,
        max_age=service.config.jwt.JWT_REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600,
    )

    await csrf_storage.delete(state)

    return TokenResponse(access_token=token.access_token)
