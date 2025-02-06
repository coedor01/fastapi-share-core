from functools import lru_cache

from celery import Celery

from fastapi_share_core.config import core_settings
from fastapi_share_core.exception import ConfigException


def check_celery():
    if any(
        [
            core_settings.celery_backend is None,
            core_settings.celery_broker is None,
        ]
    ):
        raise ConfigException("请检查Celery配置")


@lru_cache
def get_celery():
    return Celery(
        backend=core_settings.celery_backend, broker=core_settings.celery_broker
    )
