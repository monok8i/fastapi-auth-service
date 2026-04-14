from fastapi import APIRouter

from .discord import router as discord_router
from .google import router as google_router
from .tokens import router as tokens_router

router = APIRouter(prefix="/auth")
router.include_router(discord_router)
router.include_router(google_router)
router.include_router(tokens_router)

__all__ = ("router",)
