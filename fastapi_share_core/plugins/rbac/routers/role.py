from starlette import status
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi_pagination import Page

from ..data.schemas import RoleOut, RoleIn
from ..mapper.role import RoleDALDep

router = APIRouter()


@router.get("/roles", summary="获取角色列表", response_model=Page[RoleOut])
async def get_roles(dal: RoleDALDep):
    return await dal.get_page()


@router.post(
    "/roles",
    summary="新建角色",
    status_code=status.HTTP_201_CREATED,
    response_model=RoleOut,
)
async def create_role(
    dal: RoleDALDep,
    item_in: RoleIn,
):
    return await dal.create(**jsonable_encoder(item_in))


@router.put("/roles/{item_id}", summary="修改角色", response_model=RoleOut)
async def update_role(
    dal: RoleDALDep,
    item_id: int,
    item_in: RoleIn,
):
    return await dal.update(item_id, **jsonable_encoder(item_in))


@router.delete(
    "/roles/{item_id}",
    summary="删除角色",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_role(
    dal: RoleDALDep,
    item_id: int,
):
    return await dal.delete(item_id)
