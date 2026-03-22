"""JWT token service implementation."""

import secrets
import uuid
from datetime import UTC, datetime, timedelta
from typing import Any

from jose import ExpiredSignatureError, JWTError, jwt

from .config import Config as JWTConfig


class JWTTokenService:
    def __init__(
        self,
        config: JWTConfig,
    ):
        self.config = config

    def create_access_token(self, user_id: str) -> str:
        """Create access token for user."""

        return self.sign(
            {
                "sub": user_id,
                "type": "access",
            }
        )

    def create_refresh_token(self) -> str:
        """Create refresh token for user."""

        return str(uuid.uuid5(uuid.NAMESPACE_DNS, secrets.token_urlsafe(64)))

    def sign(self, payload: dict[str, str | int]) -> str:
        """Create and sign JWT token."""

        now = datetime.now(UTC)
        full_payload = payload.copy()
        full_payload.update(
            {
                "iat": int(now.timestamp()),
                "exp": int(
                    (
                        now
                        + timedelta(
                            minutes=self.config.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
                        )
                    ).timestamp()
                ),
            }
        )

        return jwt.encode(
            full_payload,
            self.config.JWT_PRIVATE_KEY,
            algorithm=self.config.JWT_ALGORITHM,
        )

    def verify(self, token: str) -> bool:
        """Verify token signature and expiration."""
        try:
            jwt.decode(
                token,
                self.config.JWT_PUBLIC_KEY,
                algorithms=[self.config.JWT_ALGORITHM],
            )
            return True
        except ExpiredSignatureError:
            return False
        except JWTError:
            return False

    def decode(self, token: str) -> dict[str, Any]:
        """Verify and return payload."""

        return jwt.decode(
            token,
            self.config.JWT_PUBLIC_KEY,
            algorithms=[self.config.JWT_ALGORITHM],
        )
