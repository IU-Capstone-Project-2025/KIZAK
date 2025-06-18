from uuid import UUID

from db.resource import (create_resource, remove_resource, retrieve_resource,
                         update_resource)
from fastapi.routing import APIRouter
from models.resource import ResourceResponse, ResourceUpdate, ResourseCreate

router = APIRouter()


@router.get(
    "/resource/{res_id}", response_model=ResourceResponse, tags=["resource"]
)
async def get_resource(res_id: UUID):
    return await retrieve_resource(res_id)


@router.post("/resource/", response_model=ResourceResponse, tags=["resource"])
async def post_resource(res: ResourseCreate):
    return await create_resource(res)


@router.put("/resource/", response_model=ResourceResponse, tags=["resource"])
async def put_resource(res: ResourceUpdate):
    return await update_resource(res)


@router.delete("/resource/{res_id}")
async def delete_resource(res_id: UUID):
    return await remove_resource(res_id)
