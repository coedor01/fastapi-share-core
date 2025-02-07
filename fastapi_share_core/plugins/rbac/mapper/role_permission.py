from typing import Annotated

from fastapi import Depends
from fastapi_share_core import dal_maker_factory, DAL
from ..data.models import RolePermission


class RolePermissionDAL(DAL[RolePermission], model=RolePermission):
    def get_page_by_role_id(self, role_id: int):
        clauses = [self.model.role_id == role_id]
        return self.get_page(clauses=clauses)

    def create_by_role_id(self, role_id: int, **kwargs):
        return self.create(role_id=role_id, **kwargs)


RolePermissionDALDep = Annotated[
    RolePermissionDAL, Depends(dal_maker_factory(RolePermissionDAL))
]
