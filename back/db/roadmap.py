from uuid import UUID

from models.roadmap import (LinkCreate, LinkResponse, NodeCreate, NodeResponse,
                            NodeUpdate, RoadmapCreate, RoadmapInfo,
                            RoadmapResponse)

from .db_connector import db


async def retrive_roadmap(roadmap_id: UUID) -> RoadmapInfo:
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
        roadmap_id,
    )

    link_rows = await db.fetch(
        """
        SELECT link_id, roadmap_id, from_node, to_node
        FROM roadmap_link
        WHERE roadmap_id = $1
        """,
        roadmap_id,
    )

    return RoadmapInfo(
        roadmap_id=roadmap_id,
        nodes=[NodeResponse(**node) for node in node_rows],
        links=[LinkResponse(**link) for link in link_rows],
    )


async def create_roadmap(roadmap: RoadmapCreate) -> RoadmapResponse:
    """Create new empty roadmap for user

    Args:
        roadmap (RoadmapCreate): New roadmap

    Returns:
        RoadmapResponse (RoadmapResponse): Created roadmap
    """
    row = await db.fetchrow(
        """
        INSERT INTO user_roadmap (user_id)
        VALUES ($1)
        RETURNING *
    """,
        roadmap.user_id,
    )

    return RoadmapResponse(**row)


async def remove_roadmap(roadmap_id: UUID) -> bool:
    """Removes roadmap from DB

    Args:
        roadmap_id (UUID): Roadmap ID

    Returns:
        bool: True if the roadmap was removed, False if no roadmap was found with that ID.
    """
    row = await db.execute(
        """
        DELETE FROM user_roadmap
        WHERE roadmap_id = $1
        """,
        roadmap_id,
    )
    return row is not None


async def retrieve_node(node_id: UUID) -> NodeResponse:
    """Retrieve a node from the roadmap

    Args:
        node_id (UUID): Node ID

    Returns:
        NodeResponse (NodeResponse): Retrieved node
    """
    row = await db.fetchrow(
        """
        SELECT *
        FROM roadmap_node
        WHERE node_id = $1
    """,
        node_id,
    )

    return NodeResponse(**row)


async def create_node(node: NodeCreate) -> NodeResponse:
    """Create a new node in the roadmap

    Args:
        node (NodeCreate): New node data

    Returns:
        NodeResponse (NodeResponse): Created node
    """
    row = await db.fetchrow(
        """
        INSERT INTO roadmap_node (roadmap_id, title, summary, resource_id, progress)
        VALUES ($1, $2, $3, $4, $5)
        RETURNING *
    """,
        node.roadmap_id,
        node.title,
        node.summary,
        node.resource_id,
        node.progress,
    )

    return NodeResponse(**row)


async def update_node(node: NodeUpdate) -> NodeResponse:
    """Update a node in the roadmap

    Args:
        node (NodeUpdate): Updated node data
    """
    values = []
    updates = []
    fields = {
        "roadmap_id": node.roadmap_id,
        "title": node.title,
        "summary": node.summary,
        "resource_id": node.resource_id,
        "progress": node.progress,
    }
    for field, value in fields.items():
        if value is not None:
            updates.append(f"{field} = ${len(updates) + 1}")
            values.append(value)

    row = await db.execute(
        f"""
        UPDATE roadmap_node
        SET {', '.join(updates)}
        WHERE node_id = $6
        RETURNING *
    """,
        *values,
        node.node_id,
    )

    return NodeResponse(**row)


async def delete_node(node_id: UUID) -> bool:
    """Delete a node from the roadmap

    Args:
        node_id (UUID): Node ID

    Returns:
        bool: True if the node was deleted, False if no node was found with that ID.
    """
    row = await db.execute(
        """
        DELETE FROM roadmap_node
        WHERE node_id = $1
    """,
        node_id,
    )

    return row is not None


async def retrieve_link(link_id: UUID) -> LinkResponse:
    """Retrieve a link from the roadmap

    Args:
        link_id (UUID): Link ID

    Returns:
        LinkResponse (LinkResponse): Retrieved link
    """
    row = await db.fetchrow(
        """
        SELECT *
        FROM roadmap_link
        WHERE link_id = $1
    """,
        link_id,
    )

    return LinkResponse(**row)


async def create_link(link: LinkCreate) -> LinkResponse:
    """Create a new link in the roadmap

    Args:
        link (LinkCreate): New link data

    Returns:
        LinkResponse (LinkResponse): Created link
    """
    row = await db.fetchrow(
        """
        INSERT INTO roadmap_link (roadmap_id, from_node, to_node)
        VALUES ($1, $2, $3)
        RETURNING *
    """,
        link.roadmap_id,
        link.from_node,
        link.to_node,
    )

    return LinkResponse(**row)


async def delete_link(link_id: UUID) -> bool:
    """Delete a link from the roadmap

    Args:
        link_id (UUID): Link ID

    Returns:
        bool: True if the link was deleted, False if no link was found with that ID.
    """
    result = await db.execute(
        """
        DELETE FROM roadmap_link
        WHERE link_id = $1
        RETURNING link_id
    """,
        link_id,
    )

    return result is not None
