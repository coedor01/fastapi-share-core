import redis.asyncio as aioredis
from functools import lru_cache
from fastapi_share_core.config import core_settings
from fastapi_share_core.exception import ConfigException


def check_redis():
    if any(
        [
            core_settings.redis_host is None,
            core_settings.redis_port is None,
        ]
    ):
        raise ConfigException("请检查Redis配置")


@lru_cache()
def get_redis() -> aioredis.Redis:
    return aioredis.Redis(
        host=core_settings.REDIS_HOST,
        port=core_settings.REDIS_PORT,
        password=core_settings.REDIS_PASSWORD,
        max_connections=core_settings.REDIS_MAX_CONNECTIONS,
        decode_responses=True,
    )
