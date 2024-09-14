from fastapi import APIRouter

from .entries import router as entries_router

router = APIRouter(
    prefix="/v1",
)
router.include_router(entries_router)
