from fastapi.routing import APIRouter
from fastapi import FastAPI

router = APIRouter()

from .v1 import router as v1_router

router.include_router(
    v1_router,
    prefix="/v1",
)


class API:
    @staticmethod
    def create() -> FastAPI:
        api = FastAPI(
            title="My API",
        )
        api.include_router(router)
        return api
