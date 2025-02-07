from starlette import status
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi_pagination import Page

from ..data.schemas import PermissionOut, PermissionIn
from ..mapper.role_permission import RolePermissionDALDep

router = APIRouter()


@router.get(
    "/roles/{role_id}/permissions",
    summary="获取指定角色的所有权限",
    response_model=Page[PermissionOut],
)
async def get_role_permissions(
    dal: RolePermissionDALDep,
    role_id: int,
):
    return await dal.get_page_by_role_id(role_id)


@router.post(
    "/roles/{role_id}/permissions",
    summary="给指定角色添加权限",
    response_model=PermissionOut,
)
async def create_role_permissions(
    dal: RolePermissionDALDep, role_id: int, item_in: PermissionIn
):
    return await dal.create_by_role_id(role_id, **jsonable_encoder(item_in))


@router.put(
    "/roles/permissions/{permission_id}",
    summary="修改指定权限",
    response_model=PermissionOut,
)
async def update_role_permission(
    dal: RolePermissionDALDep, permission_id: int, item_in: PermissionIn
):
    return await dal.update(permission_id, **jsonable_encoder(item_in))


@router.delete(
    "/roles/permissions/{permission_id}",
    summary="删除指定权限",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_role_permission(dal: RolePermissionDALDep, permission_id: int):
    return await dal.delete(permission_id)
