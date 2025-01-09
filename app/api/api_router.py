from fastapi import APIRouter

from app.api import post_router, user_router,comment_router,favorite_router,image_router,friend_router

router = APIRouter()


router.include_router(user_router.router, tags=["user"], prefix="/users")
router.include_router(post_router.router, tags=["post"], prefix="/posts")
router.include_router(comment_router.router, tags=["comment"], prefix="/comments")
router.include_router(favorite_router.router, tags=["favorite"], prefix="/favorites")
router.include_router(image_router.router, tags=["image"], prefix="/images")
router.include_router(friend_router.router, tags=["friend"], prefix="/friends")
