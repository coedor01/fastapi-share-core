from pydantic import BaseModel


class RoleIn(BaseModel):
    name: str


class RoleOut(BaseModel):
    id: int
    name: str


class PermissionIn(BaseModel):
    permission: str


class PermissionOut(BaseModel):
    id: int
    permission: str
