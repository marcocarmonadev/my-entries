from fastapi.routing import APIRouter

router = APIRouter()

from .click_up import router as click_up_router

router.include_router(
    click_up_router,
    prefix="/click-up",
)
