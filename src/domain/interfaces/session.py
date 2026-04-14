"""Session service interface."""

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from src.domain.entities.token import Token


class ISessionService(Protocol):
    async def refresh(
        self, refresh_token: str | None, ip_address: str
    ) -> "Token":
        """Refresh the user's access token using the refresh token."""
        ...

    async def logout(self, refresh_token: str | None) -> None:
        """Logout the user by deleting their refresh token."""
        ...
