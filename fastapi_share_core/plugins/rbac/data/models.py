import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from fastapi_share_core import Base


class Role(Base):
    __tablename__ = "rbac_role"

    name: Mapped[str] = mapped_column(sa.String(255), comment="名称")


class RolePermission(Base):
    __tablename__ = "rbac_role_permission"

    role_id: Mapped[int] = mapped_column(comment="角色Id")
    permission: Mapped[str] = mapped_column(sa.String(255), comment="权限标识")
