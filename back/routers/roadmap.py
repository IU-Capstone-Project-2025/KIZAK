from fastapi.routing import APIRouter
from uuid import UUID
from models.roadmap import RoadmapResponse,RoadmapCreate
from models.roadmap import NodeResponse, NodeCreate, NodeUpdate
from models.roadmap import LinkResponse, LinkCreate
from db.roadmap import retrive_roadmap, create_roadmap, remove_roadmap
from db.roadmap import retrieve_node, create_node, update_node, delete_node
from db.roadmap import retrieve_link, create_link, delete_link

router = APIRouter()

# Roadmap
@router.get("/roadmap/{roadmap_id}", response_model=RoadmapResponse, tags=["Roadmap"])
async def get_roadmap(roadmap_id: UUID) -> RoadmapResponse:
    return await retrive_roadmap(roadmap_id)

@router.post("/roadmap/", tags=["Roadmap"], response_model=RoadmapResponse)
async def post_roadmap(roadmap: RoadmapCreate) -> RoadmapResponse:
    return await create_roadmap(roadmap)

@router.delete("/roadmap/{roadmap_id}", tags=["Roadmap"])
async def get_roadmap(roadmap_id: UUID) -> None:
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
async def delete_node(node_id: UUID) -> None:
    return await delete_node(node_id)

# Links
@router.get("/link/{link_id}", response_model=LinkResponse, tags=["Link"])
async def get_link(link_id: UUID) -> LinkResponse:
    return await retrieve_link(link_id)

@router.post("/link/", response_model=LinkResponse, tags=["Link"])
async def post_link(link: LinkCreate) -> LinkResponse:
    return await create_link(link)

@router.delete("/link/", tags=["Link"])
async def delete_link(link_id: UUID) -> None:
    return await delete_link(link_id)
