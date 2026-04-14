from fastapi import APIRouter

from .discord import router as discord_router
from .github import router as github_router
from .google import router as google_router
from .tokens import router as tokens_router

router = APIRouter(prefix="/auth")
router.include_router(discord_router)
router.include_router(github_router)
router.include_router(google_router)
router.include_router(tokens_router)

__all__ = ("router",)
