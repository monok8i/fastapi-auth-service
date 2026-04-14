"""Google entities."""

from dataclasses import dataclass


@dataclass
class GoogleJWTTokenData:
    iss: str
    azp: str
    aud: str
    sub: str
    at_hash: str
    email: str
    email_verified: str
    iat: int
    exp: int
    hd: str | None = None
    nonce: str | None = None


@dataclass
class GoogleTokenData:
    access_token: str
    expires_in: int
    id_token: str
    scope: str
    token_type: str
    refresh_token: str | None = None


@dataclass
class GoogleUser:
    id: str
