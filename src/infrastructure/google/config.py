"""Google authentication configuration."""

from src.core.config import BaseEnvConfig


class Config(BaseEnvConfig):
    GOOGLE_AUTH_CLIENT_ID: str
    GOOGLE_AUTH_CLIENT_SECRET: str
    GOOGLE_AUTH_REDIRECT_URI: str
