"""Redis client factory."""

from redis.asyncio import Redis

from .config import Config as RedisConfig


def create_redis_client(config: RedisConfig) -> Redis:
    """Create and return a configured Redis client."""

    return Redis(
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
        db=config.REDIS_DB,
        password=config.REDIS_PASSWORD,
        retry_on_timeout=True,
        socket_connect_timeout=config.REDIS_SOCKET_TIMEOUT_SECONDS,
        socket_timeout=config.REDIS_SOCKET_TIMEOUT_SECONDS,
        health_check_interval=30,
        decode_responses=True,
    )
