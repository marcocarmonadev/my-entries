from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from .routers import router as api_router

api = FastAPI(
    default_response_class=ORJSONResponse,
)
api.include_router(api_router)
