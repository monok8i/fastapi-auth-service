"""Google-related exceptions."""

from src.domain.exceptions.base import AuthError


class GoogleAuthError(AuthError):
    """Base class for Google authentication errors."""


class CSRFTokenNotProvidedError(GoogleAuthError):
    """Raised when the CSRF token is not provided in the authorization URL generation."""  # noqa: E501


class NonceNotProvidedError(GoogleAuthError):
    """Raised when the nonce is not provided in the authorization URL generation."""  # noqa: E501


class AuthorizationCodeNotProvidedError(GoogleAuthError):
    """Raised when the authorization code is not provided in the callback."""


class GoogleAPIError(GoogleAuthError):
    """Raised when there is an error while communicating with the Google API."""  # noqa: E501


class UserInfoRetrievalError(GoogleAuthError):
    """Raised when there is an error while retrieving user info from Google."""


class TokenExchangeError(GoogleAuthError):
    """Raised when there is an error while exchanging the authorization code for tokens."""  # noqa: E501
