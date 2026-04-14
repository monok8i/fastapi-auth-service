"""Github authentication configuration."""

from src.core.config import BaseEnvConfig


class Config(BaseEnvConfig):
    GITHUB_AUTH_CLIENT_ID: str
    GITHUB_AUTH_CLIENT_SECRET: str
    GITHUB_AUTH_REDIRECT_URI: str
