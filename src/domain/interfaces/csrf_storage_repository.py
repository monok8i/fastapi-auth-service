"""Interface for base storage services."""

from typing import Any, Protocol


class ICSRFStorageRepository(Protocol):
    async def create(
        self, csrf_token: str, nonce: str, provider: str, ttl: int
    ) -> Any:
        """Store a CSRF token in the storage with TTL."""
        ...

    async def get(self, csrf_token: str) -> Any:
        """Return whether a CSRF token exists in the storage."""
        ...

    async def delete(self, csrf_token: str) -> None:
        """Delete a CSRF token from the storage."""
        ...
