"""Authentication endpoints."""

from fastapi import APIRouter, Request, Response, status

from src.api.dependencies import SessionServiceDependency
from src.api.schemas import Token as TokenResponse

router = APIRouter()


@router.post(
    "/refresh", status_code=status.HTTP_200_OK, response_model=TokenResponse
)
async def refresh(
    request: Request, response: Response, service: SessionServiceDependency
):
    """Refresh access token by refresh token."""
    refresh_token = request.cookies.get("refresh_token")
    ip_address = request.client.host if request.client else "unknown"

    token = await service.refresh(
        refresh_token=refresh_token, ip_address=ip_address
    )

    response.set_cookie(
        "refresh_token",
        token.refresh_token,
        httponly=True,
        max_age=service.config.jwt.JWT_REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600,
    )

    return TokenResponse(access_token=token.access_token)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    request: Request, response: Response, service: SessionServiceDependency
) -> None:
    """Logout user by refresh token."""

    refresh_token = request.cookies.get("refresh_token")

    response.delete_cookie("refresh_token", httponly=True)

    await service.logout(refresh_token=refresh_token)
