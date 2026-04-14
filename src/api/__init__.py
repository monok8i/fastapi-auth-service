from fastapi import APIRouter

from .routes.auth import router as auth_router

# including routers to main api router
router = APIRouter(prefix="/api")
router.include_router(auth_router, tags=["authentication"])

__all__ = ("router",)
