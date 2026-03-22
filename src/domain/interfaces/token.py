"""Interface for services that can be used in the OIC flow."""

from typing import Any, Protocol
from uuid import UUID


class ITokenService(Protocol):
    def create_access_token(self, user_id: str) -> str:
        """Create access token for user."""
        ...

    def create_refresh_token(self) -> str:
        """Create refresh token for user."""
        ...

    def sign(self, payload: dict[str, Any]) -> str:
        """Create and sign JWT token."""
        ...

    def verify(self, token: str) -> bool:
        """Verify token signature and expiration."""
        ...

    def decode(self, token: str) -> dict[str, Any]:
        """Verify and return payload."""
        ...
