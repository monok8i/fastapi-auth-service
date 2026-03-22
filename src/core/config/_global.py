"""Global configuration for the application."""

from functools import cached_property

from src.core.security.config import Config as JWTConfig
from src.infrastructure.discord.config import Config as DiscordConfig
from src.infrastructure.redis.config import Config as RedisConfig


class Config:
    @cached_property
    def jwt(self) -> JWTConfig:
        """Return the JWT configuration settings."""
        return JWTConfig()  # type: ignore

    @cached_property
    def discord(self) -> DiscordConfig:
        """Return the Discord configuration settings."""
        return DiscordConfig()  # type: ignore

    @cached_property
    def redis(self) -> RedisConfig:
        """Return the Redis configuration settings."""
        return RedisConfig()  # type: ignore
