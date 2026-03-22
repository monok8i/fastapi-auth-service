"""JWT entities."""

from dataclasses import dataclass


@dataclass
class JWTPayload:
    sub: str
    iat: int
    exp: int
