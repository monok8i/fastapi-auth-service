from fastapi import APIRouter

from .routes import auth

# including routers to main api router
api_router = APIRouter(prefix="/api")
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])

__all__ = ["api_router"]
