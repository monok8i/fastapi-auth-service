"""JWT configuration."""

from src.core.config.env import BaseEnvConfig


class Config(BaseEnvConfig):
    """JWT configuration."""

    JWT_PUBLIC_KEY: str
    JWT_PRIVATE_KEY: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 5
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 30
