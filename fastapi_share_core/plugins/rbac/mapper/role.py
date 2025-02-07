from typing import Annotated

from fastapi import Depends
from fastapi_share_core import dal_maker_factory, DAL
from ..data.models import Role


class RoleDAL(DAL[Role], model=Role): ...


RoleDALDep = Annotated[RoleDAL, Depends(dal_maker_factory(RoleDAL))]
