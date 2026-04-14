"""Secrets management utilities."""

import secrets


def generate_secret(length: int = 32) -> str:
    """Generate a secure random secret string."""

    return secrets.token_urlsafe(length)
