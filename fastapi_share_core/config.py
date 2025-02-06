from typing import Literal

from sqlalchemy import URL
from pydantic import Field
from pydantic_settings import BaseSettings


class CoreSettings(BaseSettings):
    app_name: str = Field("MyApp", description="应用名称")
    env: Literal["development", "test", "production"] = Field(
        "production", description="环境"
    )
    log_save_path: str = Field("logs", description="日志保存路径")
    db_host: str | None = Field(None, description="数据库地址")
    db_port: int | None = Field(None, description="数据库端口")
    db_name: str | None = Field(None, description="数据库名称")
    db_username: str | None = Field(None, description="数据库用户名")
    db_password: str | None = Field(None, description="数据库密码")
    db_pool_size: int = Field(1024, description="数据库连接池大小")
    db_max_overflow: int = Field(1024, description="数据库连接池溢出余量")
    db_echo: bool = Field(False, description="数据库是否打印执行语句")
    db_pool_pre_ping: bool = Field(True, description="数据库使用链接前是否需要ping")
    db_pool_recycle: int = Field(1800, description="数据库会话池更新周期，单位：秒")
    db_alembic_cfg_filename: str = Field(
        "alembic.ini", description="alembic配置文件名称"
    )
    db_alembic_script_location: str = Field(
        "migrations", description="alembic配置文件名称"
    )
    redis_host: str | None = Field(None, description="Redis服务IP")
    redis_port: int | None = Field(None, description="Redis服务端口")
    redis_password: str | None = Field(None, description="Redis服务密码")
    redis_max_connections: int = Field(1024, description="Redis客户端最大连接数量")

    @property
    def sqlalchemy_uri(self) -> URL:
        return URL.create(
            "mysql+asyncmy",
            host=self.db_host,
            port=self.db_port,
            username=self.db_username,
            password=self.db_password,
            database=self.db_name,
        )

    @property
    def sqlalchemy_uri_without_db(self) -> URL:
        return URL.create(
            "mysql+asyncmy",
            host=self.db_host,
            port=self.db_port,
            username=self.db_username,
            password=self.db_password,
        )

    class Config:
        case_sensitive = True
        env_file = "env/core.env"


core_settings = CoreSettings()
