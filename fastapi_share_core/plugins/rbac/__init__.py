from fastapi import APIRouter
from .routers import role
from .routers import role_permission

__all__ = ["router"]

router = APIRouter()
router.include_router(role.router)
router.include_router(role_permission.router)
