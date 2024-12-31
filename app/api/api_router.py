from fastapi import APIRouter

from app.api import post_router, user_router

router = APIRouter()


router.include_router(user_router.router, tags=["user"], prefix="/users")
router.include_router(post_router.router, tags=["post"], prefix="/posts")
