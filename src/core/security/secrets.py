"""Secrets management utilities."""

import base64
import hashlib
import secrets


def generate_secret(length: int = 32) -> str:
    """Generate a secure random secret string."""

    return secrets.token_urlsafe(length)


def generate_pkce_pair() -> tuple[str, str]:
    """Generate PKCE code_verifier and S256 code_challenge."""

    code_verifier = generate_secret(64)
    digest = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    code_challenge = (
        base64.urlsafe_b64encode(digest).decode("utf-8").rstrip("=")
    )

    return code_verifier, code_challenge
