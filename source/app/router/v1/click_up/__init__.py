from fastapi.datastructures import UploadFile
from fastapi.param_functions import Depends
from fastapi.routing import APIRouter
from starlette.status import HTTP_201_CREATED

from ....controllers import ClickUpHttpController, Factory
from ....schemas import Tag

router = APIRouter()


@router.post(
    path="/home-space/super-list/purchases",
    tags=[Tag.ClickUp],
    status_code=HTTP_201_CREATED,
)
async def register_super_purchases(
    file: UploadFile,
    controller: ClickUpHttpController = Depends(
        dependency=Factory.create_click_up_http_controller,
    ),
):
    return await controller.register_super_purchases(
        xlsx_bytes=await file.read(),
    )
