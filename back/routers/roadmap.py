from uuid import UUID
from utils.logger import logger
from fastapi import Response, status, HTTPException

from services.roadmap_genaretor import update_roadmap, generate_roadmap

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
    retrieve_roadmap_by_login,
    retrieve_roadmap_by_user_id
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
    RoadmapFeedback
)

from db.user import retrieve_user_profile

router = APIRouter()


# Roadmap
@router.get(
    "/roadmap/{roadmap_id}",
    response_model=RoadmapInfo,
    tags=["Roadmap"],
    description="Get roadmap",
    status_code=status.HTTP_200_OK
)
async def get_roadmap(roadmap_id: UUID) -> RoadmapInfo:
    logger.info(f"Getting roadmap {roadmap_id}")
    return await retrieve_roadmap(roadmap_id)


@router.get(
    "/roadmap_by_user_id/{user_id}",
    response_model=RoadmapInfo,
    tags=["Roadmap"],
    description="Get roadmap by user id",
    status_code=status.HTTP_200_OK
)
async def get_roadmap_by_user_id(user_id: UUID) -> RoadmapInfo:
    logger.info(f"Getting roadmap by user id {user_id}")
    return await retrieve_roadmap_by_user_id(user_id)


@router.get(
    "/roadmap_by_login/{login}",
    response_model=RoadmapInfo,
    tags=["Roadmap"],
    description="Get roadmap by user login",
    status_code=status.HTTP_200_OK
)
async def get_roadmap_by_login(login: str) -> RoadmapInfo:
    logger.info(f"Getting roadmap by login {login}")
    return await retrieve_roadmap_by_login(login)


@router.post(
    "/roadmap/",
    tags=["Roadmap"],
    response_model=RoadmapResponse,
    # description="Create new roadmap",
    description="Create and generate roadmap using ML generator",
    status_code=status.HTTP_201_CREATED
)
# async def post_roadmap(
#     new_roadmap: RoadmapCreate, response: Response
# ) -> RoadmapResponse:
#     roadmap = await create_roadmap(new_roadmap)
#     logger.info(f"Created roadmap {roadmap.roadmap_id}")
#     response.headers["Location"] = f"/roadmap/{roadmap.roadmap_id}"
#     return roadmap

async def post_roadmap(
    new_roadmap: RoadmapCreate
    # response: Response
) -> RoadmapInfo:
    logger.info(f"Generating roadmap for user {new_roadmap.user_id}")

    # get user profile
    profile = await retrieve_user_profile(new_roadmap.user_id)

    # formatting for generator
    user_role = profile.user.goal_vacancy
    user_query = profile.user.goals
    user_skills = profile.user.skills

    # generate from ml
    roadmap_info = await generate_roadmap(
        user_id=new_roadmap.user_id,
        user_role=user_role,
        user_skills=user_skills,
        user_query=user_query
    )

    if roadmap_info is None:
        logger.error("Roadmap generation failed")
        raise HTTPException(status_code=500, detail="Roadmap generation failed")

    logger.info(f"Roadmap generated with ID {roadmap_info.roadmap_id}")
    return roadmap_info


@router.post(
    "/update_roadmap/",
    response_model=RoadmapResponse,
    description="Update roadmap based on feedback",
    status_code=status.HTTP_201_CREATED
)
async def update_roadmap_feedback(
    data: RoadmapFeedback
):
    roadmap = await update_roadmap(data)
    logger.info(f"Updated roadmap {roadmap.roadmap_id}")
    return roadmap

@router.delete(
    "/roadmap/{roadmap_id}",
    tags=["Roadmap"],
    description="Delete roadmap",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_roadmap(roadmap_id: UUID) -> None:
    logger.info(f"Deleting roadmap {roadmap_id}")
    return await remove_roadmap(roadmap_id)


# Nodes
@router.get(
    "/node/{node_id}",
    response_model=NodeResponse,
    tags=["Node"],
    description="Get node",
    status_code=status.HTTP_200_OK
)
async def get_node(node_id: UUID) -> NodeResponse:
    logger.info(f"Getting node {node_id}")
    return await retrieve_node(node_id)


@router.post(
    "/node/",
    response_model=NodeResponse,
    tags=["Node"],
    description="Create node",
    status_code=status.HTTP_201_CREATED
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
    description="Update node",
    status_code=status.HTTP_200_OK
)
async def put_node(node: NodeUpdate) -> NodeResponse:
    logger.info(f"Updating node {node.node_id}")
    return await update_node(node)


@router.delete(
    "/node/{node_id}",
    tags=["Node"],
    description="Delete node",
    status_code=status.HTTP_204_NO_CONTENT
)
async def remove_node(node_id: UUID) -> None:
    logger.info(f"Removing node {node_id}")
    return await delete_node(node_id)


# Links
@router.get(
    "/link/{link_id}",
    response_model=LinkResponse,
    tags=["Link"],
    description="Get link",
    status_code=status.HTTP_200_OK
)
async def get_link(link_id: UUID) -> LinkResponse:
    logger.info(f"Getting link {link_id}")
    return await retrieve_link(link_id)


@router.post(
    "/link/",
    response_model=LinkResponse,
    tags=["Link"],
    description="Create link",
    status_code=status.HTTP_201_CREATED
)
async def post_link(new_link: LinkCreate, response: Response) -> LinkResponse:
    link = await create_link(new_link)
    logger.info(f"Created link {link.link_id}")
    response.headers["Location"] = f"/link/{link.link_id}"
    return link


@router.delete(
    "/link/{link_id}",
    tags=["Link"],
    description="Delete link",
    status_code=status.HTTP_204_NO_CONTENT
)
async def remove_link(link_id: UUID) -> None:
    logger.info(f"Removing link {link_id}")
    return await delete_link(link_id)
