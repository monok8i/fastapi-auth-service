"""Google OAuth provider implementation."""

import base64
import json
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

from .config import Config as GoogleConfig
from .models import GoogleJWTTokenData, GoogleTokenData, GoogleUser


class GoogleOAuthProvider(IOAuthProvider):
    def __init__(self, config: GoogleConfig):
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
            raise NonceNotProvidedError(
                "Nonce not provided in the authorization URL generation"
            )

        query = urlencode(
            {
                "client_id": self.config.GOOGLE_AUTH_CLIENT_ID,
                "redirect_uri": self.config.GOOGLE_AUTH_REDIRECT_URI,
                "response_type": "code",
                "state": csrf_token,
                "nonce": nonce,
                "scope": "openid email",
            }
        )

        return f"https://accounts.google.com/o/oauth2/v2/auth?{query}"

    async def exchange_code(
        self, code: str | None, code_verifier: str | None = None
    ) -> GoogleTokenData:
        """Exchange the authorization code for an access token."""

        _ = code_verifier

        if not code:
            raise AuthorizationCodeNotProvidedError(
                "Authorization code not provided in the callback"
            )

        try:
            async with (
                aiohttp.ClientSession() as session,
                session.post(
                    "https://oauth2.googleapis.com/token",
                    data={
                        "client_id": self.config.GOOGLE_AUTH_CLIENT_ID,
                        "client_secret": self.config.GOOGLE_AUTH_CLIENT_SECRET,
                        "grant_type": "authorization_code",
                        "code": code,
                        "redirect_uri": self.config.GOOGLE_AUTH_REDIRECT_URI,
                    },
                    headers={
                        "Content-Type": "application/x-www-form-urlencoded"
                    },
                ) as response,
            ):
                data = await response.json()

                if response.status != 200:
                    raise TokenExchangeError(
                        f"Google API error ({response.status}): {data}"
                    )

                try:
                    return GoogleTokenData(**data)
                except TypeError as e:
                    raise TokenExchangeError(
                        "Invalid token data received from Google"
                    ) from e

        except aiohttp.ClientError as e:
            raise ExternalAPIError(
                "Failed to communicate with Google API"
            ) from e

    async def get_user_info(self, token_data: GoogleTokenData) -> GoogleUser:
        """Get the user's information from the ID token."""

        id_token = token_data.id_token

        payload = id_token.split(".")[1]
        payload += "=" * (-len(payload) % 4)

        try:
            decoded_payload = base64.urlsafe_b64decode(payload)
            token_claims = GoogleJWTTokenData(**json.loads(decoded_payload))
            return GoogleUser(id=token_claims.sub)

        except (IndexError, KeyError, TypeError, ValueError) as e:
            raise UserInfoRetrievalError("Failed to decode ID token") from e
