"""Github-related exceptions."""

from src.domain.exceptions.base import AuthError


class GithubAuthError(AuthError):
    """Base class for Github authentication errors."""


class CSRFTokenNotProvidedError(GithubAuthError):
    """Raised when the CSRF token is not provided in the authorization URL generation."""  # noqa: E501


class NonceNotProvidedError(GithubAuthError):
    """Raised when the nonce is not provided in the authorization URL generation."""  # noqa: E501


class AuthorizationCodeNotProvidedError(GithubAuthError):
    """Raised when the authorization code is not provided in the callback."""


class GithubAPIError(GithubAuthError):
    """Raised when there is an error while communicating with the Github API."""  # noqa: E501


class UserInfoRetrievalError(GithubAuthError):
    """Raised when there is an error while retrieving user info from Github."""


class TokenExchangeError(GithubAuthError):
    """Raised when there is an error while exchanging the authorization code for tokens."""  # noqa: E501
