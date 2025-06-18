from fastapi.routing import APIRouter
from models.resource import ResourceResponse, ResourseCreate, ResourceUpdate
from db.resource import retrieve_resource, create_resource, update_resource, remove_resource
from uuid import UUID

router = APIRouter()

@router.get("/resource/{res_id}", response_model=ResourceResponse)
async def get_resource(res_id: UUID):
    return await retrieve_resource(res_id)

@router.post("/resource/", response_model=ResourceResponse)
async def post_resource(res: ResourseCreate):
    return await create_resource(res)

@router.put("/resource/", response_model=ResourceResponse)
async def put_resource(res: ResourceUpdate):
    return await update_resource(res)

@router.delete("/resource/{res_id}")
async def delete_resource(res_id: UUID):
    return await remove_resource(res_id)
