from fastapi_share_core.meta.singleton import ThreadUnsafeSingletonMeta
from fastapi_share_core.redis import get_redis


class BaseRedisService(metaclass=ThreadUnsafeSingletonMeta):
    def __init__(self):
        self.redis = get_redis()

    def __call__(self):
        return self
