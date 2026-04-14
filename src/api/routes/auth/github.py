"""Github authentication endpoints."""

from fastapi import APIRouter, Request, Response, status
from fastapi.responses import JSONResponse, RedirectResponse

from src.api.dependencies import (
    CSRFStorageRepositoryDependency,
    OICGithubServiceDependency,
)
from src.api.schemas import Token as TokenResponse
from src.core.security.secrets import generate_pkce_pair, generate_secret

router = APIRouter(prefix="/github")


@router.get("/", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
async def github(
    service: OICGithubServiceDependency,
    csrf_storage: CSRFStorageRepositoryDependency,
) -> RedirectResponse:
    """Authenticate user by GitHub."""

    csrf_token = generate_secret(64)
    code_verifier, code_challenge = generate_pkce_pair()
    await csrf_storage.create(csrf_token, code_verifier, provider="github")

    return RedirectResponse(
        url=service.oauth_provider.get_authorization_url(
            csrf_token=csrf_token, nonce=code_challenge
        )
    )


@router.get(
    "/callback",
    status_code=status.HTTP_200_OK,
    response_model=TokenResponse,
)
async def github_callback(
    code: str,
    state: str,
    request: Request,
    response: Response,
    service: OICGithubServiceDependency,
    csrf_storage: CSRFStorageRepositoryDependency,
):
    """Handle GitHub auth callback."""

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

    if csrf_session.provider != "github":
        return JSONResponse(
            content={"detail": "Invalid OAuth provider for CSRF token"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    token = await service.login(
        code=code,
        ip_address=ip_address,
        code_verifier=csrf_session.nonce,
    )

    response.set_cookie(
        "refresh_token",
        token.refresh_token,
        httponly=True,
        max_age=service.config.jwt.JWT_REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600,
    )

    await csrf_storage.delete(state)

    return TokenResponse(access_token=token.access_token)
