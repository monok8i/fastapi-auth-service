"""Github OAuth provider implementation."""

from urllib.parse import urlencode

import aiohttp

from src.domain.exceptions.auth import (
    AuthorizationCodeNotProvidedError,
    CSRFTokenNotProvidedError,
    ExternalAPIError,
    NonceNotProvidedError,
    TokenExchangeError,
    UserInfoRetrievalError,
)
from src.domain.interfaces.oauth_provider import IOAuthProvider

from .config import Config as GithubConfig
from .models import GithubTokenData, GithubUser


class GithubOAuthProvider(IOAuthProvider):
    def __init__(self, config: GithubConfig):
        self.config = config

    def get_authorization_url(
        self, csrf_token: str | None = None, nonce: str | None = None
    ) -> str:
        """Get the URL to redirect the user to for authorization."""

        if csrf_token is None:
            raise CSRFTokenNotProvidedError(
                "CSRF token not provided in the authorization URL generation"
            )

        if nonce is None:
            raise NonceNotProvidedError("PKCE code_challenge not provided")

        query = urlencode(
            {
                "client_id": self.config.GITHUB_AUTH_CLIENT_ID,
                "redirect_uri": self.config.GITHUB_AUTH_REDIRECT_URI,
                "response_type": "code",
                "state": csrf_token,
                "scope": "read:user user:email",
                "code_challenge": nonce,
                "code_challenge_method": "S256",
            }
        )

        return f"https://github.com/login/oauth/authorize?{query}"

    async def exchange_code(
        self, code: str | None, code_verifier: str | None = None
    ) -> GithubTokenData:
        """Exchange the authorization code for an access token."""

        if not code:
            raise AuthorizationCodeNotProvidedError(
                "Authorization code not provided in the callback"
            )

        if not code_verifier:
            raise NonceNotProvidedError(
                "PKCE code_verifier not provided in the callback"
            )

        try:
            async with (
                aiohttp.ClientSession() as session,
                session.post(
                    "https://github.com/login/oauth/access_token",
                    data={
                        "client_id": self.config.GITHUB_AUTH_CLIENT_ID,
                        "client_secret": self.config.GITHUB_AUTH_CLIENT_SECRET,
                        "code": code,
                        "redirect_uri": self.config.GITHUB_AUTH_REDIRECT_URI,
                        "code_verifier": code_verifier,
                    },
                    headers={
                        "Accept": "application/json",
                        "Content-Type": "application/x-www-form-urlencoded",
                    },
                ) as response,
            ):
                data = await response.json()

                if response.status != 200:
                    raise TokenExchangeError(
                        f"Github API error ({response.status}): {data}"
                    )

                if data.get("error"):
                    raise TokenExchangeError(
                        f"Github token exchange failed: {data}"
                    )

                try:
                    return GithubTokenData(**data)
                except TypeError as e:
                    raise TokenExchangeError(
                        "Invalid token data received from Github"
                    ) from e

        except aiohttp.ClientError as e:
            raise ExternalAPIError(
                "Failed to communicate with Github API"
            ) from e

    async def get_user_info(self, token_data: GithubTokenData) -> GithubUser:
        """Get the user's information using the access token."""

        access_token = token_data.access_token

        try:
            async with (
                aiohttp.ClientSession() as session,
                session.get(
                    "https://api.github.com/user",
                    headers={
                        "Authorization": f"Bearer {access_token}",
                        "Accept": "application/vnd.github+json",
                        "X-GitHub-Api-Version": "2022-11-28",
                    },
                ) as response,
            ):
                data = await response.json()

                if response.status != 200:
                    raise UserInfoRetrievalError(
                        f"Github API error ({response.status}): {data}"
                    )

                user_id = data.get("id")
                if not user_id:
                    raise UserInfoRetrievalError(
                        "Invalid user data received from Github"
                    )

                return GithubUser(id=str(user_id))

        except aiohttp.ClientError as e:
            raise ExternalAPIError(
                "Failed to communicate with Github API"
            ) from e
