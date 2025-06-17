from .db_connector import db
from uuid import UUID
from models.roadmap import RoadmapResponse, RoadmapCreate
from models.roadmap import NodeResponse
from models.roadmap import LinkResponse

async def retrive_roadmap(roadmap_id: UUID) -> RoadmapResponse:
    """Retrive roadmap based on its id

    Args:
        roadmap_id (UUID): Roadmap ID

    Returns:
        RoadmapInfo (RoadmapInfo): Lists with nodes and links
    """
    node_rows = await db.fetch(
        """
        SELECT node_id, roadmap_id, title, summary, resource_id, progress
        FROM roadmap_node
        WHERE roadmap_id = $1
        """,
        roadmap_id
    )

    link_rows = await db.fetch(
        """
        SELECT link_id, roadmap_id, from_node, to_node
        FROM roadmap_link
        WHERE roadmap_id = $1
        """,
        roadmap_id
    )

    return RoadmapResponse(
        id=roadmap_id,
        nodes=[NodeResponse(**node) for node in node_rows],
        links=[LinkResponse(**link) for link in link_rows]
    )

async def create_roadmap(roadmap: RoadmapCreate) -> RoadmapResponse:
    """Create new empty roadmap for user

    Args:
        roadmap (RoadmapCreate): New roadmap

    Returns:
        RoadmapResponse (RoadmapResponse): Created roadmap
    """
    row = await db.fetchrow("""
        INSERT INTO user_roadmap (user_id)
        VALUES ($1)
        RETURNING *
    """, roadmap.user_id)

    return RoadmapResponse(**row)

async def remove_roadmap(roadmap_id: UUID) -> None:
    """Removes roadmap from DB

    Args:
        roadmap_id (UUID): Roadmap ID
    """
    await db.execute(
        """
        DELETE FROM user_roadmap
        WHERE roadmap_id = $1
        """,
        roadmap_id
    )
