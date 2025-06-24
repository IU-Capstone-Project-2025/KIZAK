from uuid import UUID
from utils.logger import logger
from fastapi import status

from db.resource import (
    create_resource,
    remove_resource,
    retrieve_resource,
    update_resource,
)
from fastapi.routing import APIRouter
from models.resource import ResourceCreate, ResourceResponse, ResourceUpdate

router = APIRouter()


@router.get(
    "/resource/{res_id}", 
    response_model=ResourceResponse, 
    tags=["Resource"],
    description="Gets a resource from database based on UUID",
    status_code=status.HTTP_200_OK
)
async def get_resource(res_id: UUID):
    logger.info(f"Retrieving resource {res_id}")
    return await retrieve_resource(res_id)


@router.post(
    "/resources/",
    response_model=ResourceResponse,
    tags=["Resource"],
    description="Creates new resource",
    status_code=status.HTTP_201_CREATED
)
async def post_resource(res: ResourceCreate):
    resource = await create_resource(res)
    logger.info(f"Created resource {resource.resource_id}")
    return resource


@router.put("/resources/", response_model=ResourceResponse, tags=["Resource"])
async def put_resource(res: ResourceUpdate):
    logger.info(f"Updating resource {res.resource_id}")
    return await update_resource(res)


@router.delete(
    "/resources/{res_id}",
    tags=["Resource"],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_resource(res_id: UUID):
    logger.info(f"Deleting resource {res_id}")
    return await remove_resource(res_id)
