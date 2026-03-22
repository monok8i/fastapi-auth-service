"""Discord entities."""

from dataclasses import dataclass


@dataclass
class DiscordTokenData:
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str
    scope: str


@dataclass
class DiscordUser:
    id: str
