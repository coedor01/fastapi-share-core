# fastapi-share-core

## 项目概述

`fastapi-share-core` 是一个基于 FastAPI 构建的核心项目，旨在提供一系列强大且易于使用的功能，帮助开发者快速构建高效的 Web 应用程序。该项目集成了数据库管理、Redis 缓存、Celery 任务队列等多种功能，同时使用了 Alembic 进行数据库迁移管理，为开发和部署带来了极大的便利。

## 主要功能

### 1. 数据库管理
- 使用 SQLAlchemy 作为 ORM 工具，支持异步数据库操作，提高数据库访问效率。
- 通过 Alembic 进行数据库迁移管理，确保数据库结构与代码的一致性。

### 2. Redis 缓存
- 集成 Redis 作为缓存系统，使用 `redis[asyncio]` 库实现异步缓存操作，提升应用性能。

### 3. Celery 任务队列
- 引入 Celery 实现任务队列，方便处理异步任务，如发送邮件、处理文件等。

### 4. 权限管理（RBAC）
- 提供基于角色的访问控制（RBAC）功能，通过 `Role` 和 `RolePermission` 模型管理用户权限。

## 安装与使用

### 1. 克隆项目
首先，将项目克隆到本地：
```bash
git clone <项目仓库地址>
cd fastapi-share-core
```

### 2. 安装依赖
确保你已经安装了 Python 3.10 或更高版本，然后使用 `pip` 安装项目依赖：
```bash
pip install -r requirements.txt
```

### 3. 配置环境变量
在`env`目录下创建一个 `core.env` 文件，并根据 `fastapi_share_core/config.py` 中的配置项进行配置：
```plaintext
# 应用名称
APP_NAME=MyApp
# 环境
ENV=production
# 日志保存路径
LOG_SAVE_PATH=logs
# 数据库配置
DB_HOST=localhost
DB_PORT=3306
DB_NAME=fastapi-share-core
DB_USERNAME=root
DB_PASSWORD=123456
# Redis 配置
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
REDIS_MAX_CONNECTIONS=1024
# Celery 配置
CELERY_BACKEND=redis://localhost:6379/0
CELERY_BROKER=redis://localhost:6379/0
```

### 4. 运行项目
启动 FastAPI 应用：使用pycharm运行app/main.py文件即可

## 项目结构

```
fastapi-share-core/
├── alembic.ini              # Alembic 配置文件
├── migrations/              # 数据库迁移脚本目录
├── fastapi_share_core/      # 项目主目录
│   ├── config.py            # 项目配置文件
│   ├── db.py                # 数据库核心
│   ├── redis.py             # Redis核心
│   ├── celery.py            # Celery核心
│   ├── log.py               # 日志核心
│   ├── utils.py             # 工具函数
│   ├── service/             # 服务层目录
│   │   ├── db.py                # 数据库服务
│   │   └── redis.py             # Redis服务
│   ├── exception/           # 异常
│   │   └── error.py             # 错误码
│   ├── plugins/             # 插件目录
│   │   └── rbac/            # RBAC 插件
│   │       ├── data/        # 数据模型目录
│   │       │   └── models.py
│   │       └── mapper/      # 数据访问层目录
│   │           ├── role.py
│   │           └── role_permission.py
│   └── meta/                # 元类目录
│       ├── db_service.py    # 数据库服务元类
│       └── singleton.py    # 单例元类
├── pyproject.toml           # 项目配置文件
└── README.md                # 项目说明文档
```

## 贡献指南
如果你想为 `fastapi-share-core` 项目做出贡献，欢迎提交 Pull Request。在提交之前，请确保你的代码符合以下要求：
- 代码风格遵循 PEP 8 规范。
- 所有新功能都有相应的单元测试。
- 提交的代码不包含安全漏洞。