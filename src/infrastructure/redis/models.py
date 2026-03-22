"""Redis models."""

from dataclasses import dataclass


@dataclass
class Session:
    """Session model for storing user sessions in Redis."""

    user_id: str
    ip_address: str
    refresh_token: str
    expires_in: int
