"""Exceptions for the domain layer."""


class NoCodeProviderError(Exception):
    pass


class InvalidTokenPayloadError(Exception):
    def __init__(self):
        super().__init__("Invalid token payload.")


class InvalidTokenError(Exception):
    pass


class TokenRevokedError(Exception):
    def __init__(self):
        super().__init__("Token has been revoked.")


class NoTokenProvidedError(Exception):
    def __init__(self):
        super().__init__("No token provided for user info retrieval.")


class RefreshTokenNotProvidedError(Exception):
    def __init__(self):
        super().__init__("No refresh token provided.")
