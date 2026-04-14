"""API dependencies."""

from typing import TYPE_CHECKING, Annotated

from fastapi import Depends, Request

from src.core.config._global import Config
from src.core.security.jwt import JWTTokenService
from src.infrastructure.discord.oauth_provider import DiscordOAuthProvider
from src.infrastructure.google.oauth_provider import GoogleOAuthProvider
from src.infrastructure.redis.csrf_storage_repository import (
    CSRFStorageRepository,
)
from src.infrastructure.redis.storage_repository import RedisStorageRepository
from src.services.oic import OICService
from src.services.session import SessionService

if TYPE_CHECKING:
    from redis.asyncio import Redis


def get_redis_client(request: Request) -> "Redis":
    """Get the Redis client from the request state."""
    return request.app.state.redis_client


def get_csrf_storage_repository(
    redis_client: Annotated["Redis", Depends(get_redis_client)],
) -> CSRFStorageRepository:
    """Get the CSRF storage repository."""

    return CSRFStorageRepository(redis_client)


def get_redis_storage_repository(
    redis_client: Annotated["Redis", Depends(get_redis_client)],
) -> RedisStorageRepository:
    """Get the Redis storage repository."""

    return RedisStorageRepository(redis_client)


def get_discord_oauth_provider(request: "Request") -> DiscordOAuthProvider:
    """Get the OAuth provider."""

    return DiscordOAuthProvider(request.app.state.config.discord)


def jwt_token_service(request: Request):
    """Get the JWT token service."""

    return JWTTokenService(request.app.state.config.jwt)


def get_config(request: Request) -> Config:
    """Get the global configuration."""

    return request.app.state.config


def get_google_oauth_provider(request: Request) -> GoogleOAuthProvider:
    """Get the OAuth provider."""

    return GoogleOAuthProvider(request.app.state.config.google)


def get_discord_oic_service(
    redis_storage_repository: Annotated[
        RedisStorageRepository, Depends(get_redis_storage_repository)
    ],
    discord_oauth_provider: Annotated[
        DiscordOAuthProvider, Depends(get_discord_oauth_provider)
    ],
    jwt_token_service: Annotated[JWTTokenService, Depends(jwt_token_service)],
    config: Annotated[Config, Depends(get_config)],
) -> OICService:
    """Get the OIC service."""

    return OICService(
        oauth_provider=discord_oauth_provider,
        token_service=jwt_token_service,
        storage=redis_storage_repository,
        config=config,
    )


def get_google_oic_service(
    redis_storage_repository: Annotated[
        RedisStorageRepository, Depends(get_redis_storage_repository)
    ],
    google_oauth_provider: Annotated[
        GoogleOAuthProvider, Depends(get_google_oauth_provider)
    ],
    jwt_token_service: Annotated[JWTTokenService, Depends(jwt_token_service)],
    config: Annotated[Config, Depends(get_config)],
) -> OICService:
    """Get the OIC service."""

    return OICService(
        oauth_provider=google_oauth_provider,
        token_service=jwt_token_service,
        storage=redis_storage_repository,
        config=config,
    )


def get_session_service(
    redis_storage_repository: Annotated[
        RedisStorageRepository, Depends(get_redis_storage_repository)
    ],
    jwt_token_service: Annotated[JWTTokenService, Depends(jwt_token_service)],
    config: Annotated[Config, Depends(get_config)],
) -> SessionService:
    """Get the session service."""

    return SessionService(
        storage=redis_storage_repository,
        token_service=jwt_token_service,
        config=config,
    )


CSRFStorageRepositoryDependency = Annotated[
    CSRFStorageRepository, Depends(get_csrf_storage_repository)
]

OICDiscordServiceDependency = Annotated[
    OICService, Depends(get_discord_oic_service)
]

OICGoogleServiceDependency = Annotated[
    OICService, Depends(get_google_oic_service)
]

SessionServiceDependency = Annotated[
    SessionService, Depends(get_session_service)
]
