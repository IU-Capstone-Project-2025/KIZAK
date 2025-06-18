from uuid import UUID

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
)

router = APIRouter()


# Roadmap
@router.get(
    "/roadmap/{roadmap_id}", response_model=RoadmapResponse, tags=["Roadmap"]
)
async def get_roadmap(roadmap_id: UUID) -> RoadmapResponse:
    return await retrieve_roadmap(roadmap_id)


@router.post("/roadmap/", tags=["Roadmap"], response_model=RoadmapResponse)
async def post_roadmap(roadmap: RoadmapCreate) -> RoadmapResponse:
    return await create_roadmap(roadmap)


@router.delete("/roadmap/{roadmap_id}", tags=["Roadmap"])
async def delete_roadmap(roadmap_id: UUID) -> None:
    return await remove_roadmap(roadmap_id)


# Nodes
@router.get("/node/{node_id}", response_model=NodeResponse, tags=["Node"])
async def get_node(node_id: UUID) -> NodeResponse:
    return await retrieve_node(node_id)


@router.post("/node/", response_model=NodeResponse, tags=["Node"])
async def post_node(node: NodeCreate) -> NodeResponse:
    return await create_node(node)


@router.put("/node/", response_model=NodeResponse, tags=["Node"])
async def put_node(node: NodeUpdate) -> NodeResponse:
    return await update_node(node)


@router.delete("/node/", tags=["Node"])
async def remove_node(node_id: UUID) -> None:
    return await delete_node(node_id)


# Links
@router.get("/link/{link_id}", response_model=LinkResponse, tags=["Link"])
async def get_link(link_id: UUID) -> LinkResponse:
    return await retrieve_link(link_id)


@router.post("/link/", response_model=LinkResponse, tags=["Link"])
async def post_link(link: LinkCreate) -> LinkResponse:
    return await create_link(link)


@router.delete("/link/", tags=["Link"])
async def remove_link(link_id: UUID) -> None:
    return await delete_link(link_id)
