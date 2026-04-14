"""Global configuration for the application."""

from functools import cached_property

from src.api.config import Config as APIConfig
from src.core.security.config import Config as JWTConfig
from src.infrastructure.discord.config import Config as DiscordConfig
from src.infrastructure.github.config import Config as GithubConfig
from src.infrastructure.google.config import Config as GoogleConfig
from src.infrastructure.redis.config import Config as RedisConfig


class Config:
    """Global configuration class for the application."""

    @cached_property
    def api(self) -> APIConfig:
        """Return the API configuration settings."""
        return APIConfig()  # type: ignore

    @cached_property
    def jwt(self) -> JWTConfig:
        """Return the JWT configuration settings."""
        return JWTConfig()  # type: ignore

    @cached_property
    def discord(self) -> DiscordConfig:
        """Return the Discord configuration settings."""
        return DiscordConfig()  # type: ignore

    @cached_property
    def google(self) -> GoogleConfig:
        """Return the Google configuration settings."""
        return GoogleConfig()  # type: ignore

    @cached_property
    def github(self) -> GithubConfig:
        """Return the Github configuration settings."""
        return GithubConfig()  # type: ignore

    @cached_property
    def redis(self) -> RedisConfig:
        """Return the Redis configuration settings."""
        return RedisConfig()  # type: ignore


config = Config()
