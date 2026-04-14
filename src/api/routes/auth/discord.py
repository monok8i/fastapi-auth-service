"""Discord authentication endpoints."""

from fastapi import APIRouter, Request, Response, status
from fastapi.responses import RedirectResponse

from src.api.dependencies import OICDiscordServiceDependency
from src.api.schemas import Token as TokenResponse

router = APIRouter(prefix="/discord")


@router.get("/", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
async def discord(service: OICDiscordServiceDependency) -> RedirectResponse:
    """Authenticate user by Discord."""

    return RedirectResponse(url=service.oauth_provider.get_authorization_url())


@router.get(
    "/callback",
    status_code=status.HTTP_200_OK,
    response_model=TokenResponse,
)
async def discord_callback(
    code: str,
    request: Request,
    response: Response,
    service: OICDiscordServiceDependency,
):
    """Handle Discord auth callback."""
    ip_address = request.client.host if request.client else "unknown"

    token = await service.login(code=code, ip_address=ip_address)

    response.set_cookie(
        "refresh_token",
        token.refresh_token,
        httponly=True,
        max_age=service.config.jwt.JWT_REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600,
    )

    return TokenResponse(access_token=token.access_token)
