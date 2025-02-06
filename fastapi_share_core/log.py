import sys
from pathlib import Path
from loguru import logger
from fastapi_share_core.config import core_settings


def setup_logger():
    # 创建日志目录
    log_path = Path(core_settings.log_save_path)
    log_path.mkdir(exist_ok=True)

    # 移除默认的处理器
    logger.remove()

    # 日志格式
    fmt = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    )

    # 根据环境配置不同的日志级别
    console_level = "DEBUG" if core_settings.env == "development" else "INFO"

    # 添加控制台处理器
    logger.add(sys.stdout, format=fmt, level=console_level, enqueue=True)

    if core_settings.env == "production":
        # 添加文件处理器
        logger.add(
            str(log_path / f"{core_settings.app_name}_{{time}}.log"),
            format=fmt,
            level="INFO",
            rotation="500 MB",
            retention="10 days",
            encoding="utf-8",
            enqueue=True,
        )

    return logger
