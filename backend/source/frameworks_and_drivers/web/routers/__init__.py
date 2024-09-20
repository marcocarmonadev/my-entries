from fastapi.routing import APIRouter

from .v1 import router as v1_router

router = APIRouter(
    prefix="/api",
)


@router.get(
    path="/health",
)
def get_health():
    return {
        "health": "OK",
    }


router.include_router(v1_router)
