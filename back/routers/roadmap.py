from uuid import UUID
from utils.logger import logger
from fastapi import Response, status

from db.roadmap import (
    create_link,
    create_node,
    create_roadmap,
    delete_link,
    delete_node,
    remove_roadmap,
    retrieve_link,
    retrieve_node,
    retrieve_roadmap,
    update_node,
    retrieve_roadmap_by_login
)
from fastapi.routing import APIRouter
from models.roadmap import (
    LinkCreate,
    LinkResponse,
    NodeCreate,
    NodeResponse,
    NodeUpdate,
    RoadmapCreate,
    RoadmapResponse,
    RoadmapInfo,
)

router = APIRouter()


# Roadmap
@router.get(
    "/roadmap/{roadmap_id}",
    response_model=RoadmapInfo,
    tags=["Roadmap"],
    description="Get roadmap"
)
async def get_roadmap(roadmap_id: UUID) -> RoadmapInfo:
    logger.info(f"Getting roadmap {roadmap_id}")
    return await retrieve_roadmap(roadmap_id)


@router.get(
    "/roadmap_by_login/{login}",
    response_model=RoadmapInfo,
    tags=["Roadmap"],
    description="Get roadmap by user login"
)
async def get_roadmap_by_login(login: str) -> RoadmapInfo:
    logger.info(f"Getting roadmap by login {login}")
    return await retrieve_roadmap_by_login(login)


@router.post(
    "/roadmap/",
    tags=["Roadmap"],
    response_model=RoadmapResponse,
    description="Create new roadmap",
    status_code=status.HTTP_201_CREATED
)
async def post_roadmap(
    new_roadmap: RoadmapCreate, response: Response
) -> RoadmapResponse:
    roadmap = await create_roadmap(new_roadmap)
    logger.info(f"Created roadmap {roadmap.roadmap_id}")
    response.headers["Location"] = f"/roadmap/{roadmap.roadmap_id}"
    return roadmap


@router.delete(
    "/roadmap/{roadmap_id}",
    tags=["Roadmap"],
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete roadmap"

)
async def delete_roadmap(roadmap_id: UUID) -> None:
    logger.info(f"Deleting roadmap {roadmap_id}")
    return await remove_roadmap(roadmap_id)


# Nodes
@router.get(
    "/node/{node_id}",
    response_model=NodeResponse,
    tags=["Node"],
    description="Get node"

)
async def get_node(node_id: UUID) -> NodeResponse:
    logger.info(f"Getting node {node_id}")
    return await retrieve_node(node_id)


@router.post(
    "/node/",
    response_model=NodeResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Node"],
    description="Create node"

)
async def post_node(new_node: NodeCreate, response: Response) -> NodeResponse:
    node = await create_node(new_node)
    logger.info(f"Created node {node.node_id}")
    response.headers["Location"] = f"/node/{node.node_id}"
    return node


@router.put(
    "/node/",
    response_model=NodeResponse,
    tags=["Node"],
    description="Update node"

)
async def put_node(node: NodeUpdate) -> NodeResponse:
    logger.info(f"Updating node {node.node_id}")
    return await update_node(node)


@router.delete(
    "/node/{node_id}",
    tags=["Node"],
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete node"

)
async def remove_node(node_id: UUID) -> None:
    logger.info(f"Removing node {node_id}")
    return await delete_node(node_id)


# Links
@router.get(
    "/link/{link_id}",
    response_model=LinkResponse,
    tags=["Link"],
    description="Get link"

)
async def get_link(link_id: UUID) -> LinkResponse:
    logger.info(f"Getting link {link_id}")
    return await retrieve_link(link_id)


@router.post(
    "/link/",
    response_model=LinkResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Link"],
    description="Create node"

)
async def post_link(new_link: LinkCreate, response: Response) -> LinkResponse:
    link = await create_link(new_link)
    logger.info(f"Created link {link.link_id}")
    response.headers["Location"] = f"/link/{link.link_id}"
    return link


@router.delete(
    "/link/{link_id}",
    tags=["Link"],
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete link"

)
async def remove_link(link_id: UUID) -> None:
    logger.info(f"Removing link {link_id}")
    return await delete_link(link_id)
