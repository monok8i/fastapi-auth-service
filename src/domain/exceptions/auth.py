"""Auth-related exceptions."""

from .base import AuthError


class RefreshTokenNotProvidedError(AuthError):
    """Raised when a refresh token is not provided for refreshing the access token."""  # noqa: E501


class TokenRevokedError(AuthError):
    """Raised when a refresh token is revoked or invalid."""


class AuthorizationCodeNotProvidedError(AuthError):
    """Raised when the authorization code is not provided in the callback."""


class UserInfoRetrievalError(AuthError):
    """Raised when there is an error while retrieving user info from Discord."""  # noqa: E501


class TokenExchangeError(AuthError):
    """Raised when there is an error while exchanging the authorization code for tokens."""  # noqa: E501


class CSRFTokenNotProvidedError(AuthError):
    """Raised when the CSRF token is not provided in the authorization URL generation."""  # noqa: E501


class NonceNotProvidedError(AuthError):
    """Raised when the nonce is not provided in the authorization URL generation."""  # noqa: E501


class ExternalAPIError(AuthError):
    """Raised when there is an error while communicating with the external API."""  # noqa: E501
