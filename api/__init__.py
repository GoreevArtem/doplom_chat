from fastapi import APIRouter

from . import auth, user, posts, image, admin

router = APIRouter()
router.include_router(auth.router)
router.include_router(user.router)
router.include_router(posts.router)
router.include_router(image.router)
router.include_router(admin.router)