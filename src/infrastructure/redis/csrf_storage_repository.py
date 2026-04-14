"""Interface for base storage services."""

import json
from dataclasses import asdict
from typing import TYPE_CHECKING

from redis.exceptions import ConnectionError, TimeoutError
from src.domain.interfaces.csrf_storage_repository import (
    ICSRFStorageRepository,
)

from .exceptions import RedisError
from .models import CSRFToken

if TYPE_CHECKING:
    from redis.asyncio import Redis


class CSRFStorageRepository(ICSRFStorageRepository):
    def __init__(self, client: "Redis"):
        self.client = client

    def _key(self, csrf_token: str) -> str:
        return f"csrf_token:{csrf_token}"

    def _dumps(self, value: CSRFToken) -> str:
        return json.dumps(asdict(value))

    def _loads(self, value: str) -> CSRFToken:
        return CSRFToken(**json.loads(value))

    async def create(
        self,
        csrf_token: str,
        nonce: str,
        provider: str,
        ttl: int = 300,
    ) -> CSRFToken:
        """Store CSRF token as a Redis key with expiration TTL."""

        token = CSRFToken(token=csrf_token, nonce=nonce, provider=provider)

        try:
            await self.client.set(
                self._key(csrf_token), self._dumps(token), ex=ttl
            )
        except (ConnectionError, TimeoutError) as e:
            raise RedisError("Failed to communicate with Redis storage") from e

        return token

    async def get(self, csrf_token: str) -> CSRFToken | None:
        """Get a CSRF token from Redis storage."""

        try:
            data = await self.client.get(self._key(csrf_token))
        except (ConnectionError, TimeoutError) as e:
            raise RedisError("Failed to communicate with Redis storage") from e

        if not data:
            return None

        return self._loads(data)

    async def delete(self, csrf_token: str) -> None:
        """Delete a CSRF token from Redis storage."""

        try:
            await self.client.delete(self._key(csrf_token))
        except (ConnectionError, TimeoutError) as e:
            raise RedisError("Failed to communicate with Redis storage") from e
