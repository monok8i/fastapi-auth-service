"""Discord OAuth provider implementation."""

import aiohttp

from src.domain.exceptions import NoTokenProvidedError
from src.domain.interfaces.oauth_provider import IOAuthProvider
from src.infrastructure.discord.entities import DiscordTokenData, DiscordUser

from .config import Config as DiscordConfig


class DiscordOAuthProvider(IOAuthProvider):
    def __init__(self, config: DiscordConfig):
        self.config = config

    def get_authorization_url(self):
        """Get the URL to redirect the user to for authorization."""

        return (
            f"https://discord.com/oauth2/authorize"
            f"?client_id={self.config.DISCORD_AUTH_CLIENT_ID}"
            f"&redirect_uri={self.config.DISCORD_AUTH_REDIRECT_URI}"
            f"&response_type=code&scope=identify"
        )

    async def exchange_code(self, code: str) -> DiscordTokenData:
        """Exchange the authorization code for an access token."""

        async with (
            aiohttp.ClientSession() as session,
            session.post(
                "https://discord.com/api/oauth2/token",
                data={
                    "client_id": self.config.DISCORD_AUTH_CLIENT_ID,
                    "client_secret": self.config.DISCORD_AUTH_CLIENT_SECRET,
                    "grant_type": "authorization_code",
                    "code": code,
                    "redirect_uri": self.config.DISCORD_AUTH_REDIRECT_URI,
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            ) as response,
        ):
            return DiscordTokenData(**await response.json())

    async def get_user_info(self, token_data: DiscordTokenData) -> DiscordUser:
        """Get the user's information using the access token."""

        access_token = token_data.access_token
        if not access_token:
            raise NoTokenProvidedError()

        async with (
            aiohttp.ClientSession() as session,
            session.get(
                "https://discord.com/api/users/@me",
                headers={"Authorization": f"Bearer {access_token}"},
            ) as response,
        ):
            result = await response.json()

        return DiscordUser(id=result.get("id"))

    async def refresh_token(self, refresh_token: str) -> DiscordTokenData:
        """Refresh the access token using the refresh token."""

        async with (
            aiohttp.ClientSession() as session,
            session.post(
                "https://discord.com/api/oauth2/token",
                data={
                    "client_id": self.config.DISCORD_AUTH_CLIENT_ID,
                    "client_secret": self.config.DISCORD_AUTH_CLIENT_SECRET,
                    "grant_type": "refresh_token",
                    "refresh_token": refresh_token,
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            ) as response,
        ):
            return DiscordTokenData(**await response.json())
