from fastapi import FastAPI

from .router import router

api = FastAPI()
api.include_router(
    router,
    prefix="/api",
)
