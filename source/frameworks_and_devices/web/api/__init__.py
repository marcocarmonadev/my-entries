from fastapi.applications import FastAPI
from fastapi.responses import ORJSONResponse

from .routers import router


def build():
    api = FastAPI(
        default_response_class=ORJSONResponse,
    )
    api.include_router(router)
    return api
