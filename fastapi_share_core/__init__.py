import traceback

from loguru import logger
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_pagination import add_pagination

from fastapi_share_core.celery import check_celery, get_celery
from fastapi_share_core.config import core_settings
from fastapi_share_core.db import check_db
from fastapi_share_core.redis import check_redis
from fastapi_share_core.exception import BusinessException
from fastapi_share_core.log import setup_logger
from fastapi_share_core.db import Base
from fastapi_share_core.service.db import BaseDbService
from fastapi_share_core.service.redis import BaseRedisService
from fastapi_share_core.exception.error import BaseEC

__all__ = ["add_share_core", "Base", "BaseDbService", "BaseRedisService", "BaseEC", "get_celery"]


def add_share_core(
        app: FastAPI,
        enable_db: bool = False,
        enable_redis: bool = False,
        enable_celery: bool = False,
) -> None:
    """

    Args:
        app: Fastapi实例
        enable_db: 是否使用数据库
        enable_redis: 是否使用redis
        enable_celery: 是否使用celery

    Returns:

    """
    setup_logger()
    logger.info(r"""
     _                                         
 ___| |__   __ _ _ __ ___    ___ ___  _ __ ___ 
/ __| '_ \ / _` | '__/ _ \  / __/ _ \| '__/ _ \
\__ \ | | | (_| | | |  __/ | (_| (_) | | |  __/
|___/_| |_|\__,_|_|  \___|  \___\___/|_|  \___|                    
    """)
    logger.info(f"当前环境: {core_settings.env}")
    add_pagination(app)

    @app.exception_handler(BusinessException)
    async def business_exception_handler(request: Request, exc: BusinessException):
        return JSONResponse(
            status_code=400,
            content={"detail": {"code": exc.code, "msg": exc.msg}},
        )

    @app.exception_handler(Exception)
    async def server_exception_handler(request: Request, exc: Exception):
        detail = {"code": 999999, "msg": "Server Error."}
        if core_settings.env == "development":
            detail.update({"traceback": traceback.format_exc()})

        return JSONResponse(
            status_code=500,
            content={"detail": detail},
        )

    if enable_db:
        check_db()

    if enable_redis:
        check_redis()

    if enable_celery:
        check_celery()
