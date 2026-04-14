"""Discord entities."""

from dataclasses import dataclass


@dataclass
class GithubTokenData:
    access_token: str
    token_type: str
    scope: str | None = None
    expires_in: int | None = None
    refresh_token: str | None = None


@dataclass
class GithubUser:
    id: str
