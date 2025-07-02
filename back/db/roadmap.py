from uuid import UUID

from fastapi import HTTPException
from utils.logger import logger

from models.roadmap import (
    LinkCreate,
    LinkResponse,
    NodeCreate,
    NodeResponse,
    NodeUpdate,
    RoadmapCreate,
    RoadmapInfo,
    RoadmapResponse,
)

from .db_connector import db


async def retrieve_roadmap_by_user_id(user_id: UUID) -> RoadmapInfo:
    """Retrieve roadmap based on user ID

    Args:
        user_id (UUID): User ID

    Returns:
        RoadmapInfo (RoadmapInfo): Lists with nodes and links
    """
    try:
        logger.info(f"Retrieving roadmap of user {user_id}")
        roadmap_row = await db.fetchrow(
            """
            SELECT roadmap_id, user_id
            FROM user_roadmap
            WHERE user_id = $1
            """,
            user_id,
        )

        if not roadmap_row:
            raise HTTPException(
                status_code=404,
                detail=f"Roadmap for user {user_id} not exists"
            )
    except HTTPException:
        raise
    return await retrieve_roadmap(roadmap_row['roadmap_id'])


async def retrieve_roadmap(roadmap_id: UUID) -> RoadmapInfo:
    """Retrieve roadmap based on its id

    Args:
        roadmap_id (UUID): Roadmap ID

    Returns:
        RoadmapInfo (RoadmapInfo): Lists with nodes and links
    """
    async with db.transaction() as conn:
        roadmap_exists = await conn.fetchrow(
            """
            SELECT 1 FROM user_roadmap WHERE roadmap_id = $1
            """,
            roadmap_id,
        )

        if not roadmap_exists:
            logger.error(f"Roadmap {roadmap_id} not found")
            raise HTTPException(status_code=404, detail="Roadmap not found")

        logger.info(f"Retrieving nodes of the roadmap {roadmap_id}")
        node_rows = await conn.fetch(
            """
            SELECT node_id, roadmap_id, title, summary, resource_id, progress
            FROM roadmap_node
            WHERE roadmap_id = $1
            """,
            roadmap_id,
        )
        logger.info(f"Retrieved nodes of the roadmap {roadmap_id}")

        logger.info(f"Retrieving links of the roadmap {roadmap_id}")
        link_rows = await conn.fetch(
            """
            SELECT link_id, roadmap_id, from_node, to_node
            FROM roadmap_link
            WHERE roadmap_id = $1
            """,
            roadmap_id,
        )
        logger.info(f"Retrieved links of the roadmap {roadmap_id}")

        logger.info(f"Retrieving roadmap {roadmap_id} retrieved successfully")
    return RoadmapInfo(
        roadmap_id=roadmap_id,
        nodes=[NodeResponse(**node) for node in node_rows],
        links=[LinkResponse(**link) for link in link_rows],
    )


async def retrieve_roadmap_by_login(login: str) -> RoadmapInfo:
    """Retrieve roadmap based on user login

    Args:
        login (str): User login

    Returns:
        RoadmapInfo (RoadmapInfo): Lists with nodes and links
    """
    logger.info(f"Retrieving roadmap by login {login}")
    user_row = await db.fetchrow(
        """
        SELECT user_id
        FROM users
        WHERE login = $1
        """,
        login,
    )
    if not user_row:
        logger.error(f"User {login} not found")
        raise HTTPException(status_code=404, detail="User not found")
    roadmap_row = await db.fetchrow(
        """
        SELECT roadmap_id
        FROM user_roadmap
        WHERE user_id = $1
        """,
        user_row["user_id"],
    )

    roadmap_id = roadmap_row["roadmap_id"]
    return await retrieve_roadmap(roadmap_id)


async def create_roadmap(roadmap: RoadmapCreate) -> RoadmapResponse:
    """Create new empty roadmap for user

    Args:
        roadmap (RoadmapCreate): New roadmap

    Returns:
        RoadmapResponse (RoadmapResponse): Created roadmap
    """
    async with db.transaction() as conn:
        logger.info(f"Creating new roadmap for user {roadmap.user_id}")
        row = await conn.fetchrow(
            """
            INSERT INTO user_roadmap (user_id)
            VALUES ($1)
            RETURNING *
        """,
            roadmap.user_id,
        )

        if not row:
            logger.error("Failed to create roadmap")
            raise HTTPException(status_code=500,
                                detail="Failed to create roadmap")

    return RoadmapResponse(**row)


async def remove_roadmap(roadmap_id: UUID):
    """Removes roadmap from DB

    Args:
        roadmap_id (UUID): Roadmap ID

    """
    async with db.transaction() as conn:
        row = await conn.execute(
            """
            DELETE FROM user_roadmap
            WHERE roadmap_id = $1
            """,
            roadmap_id,
        )
        if row == "DELETE 0":
            logger.error(f"Roadmap {roadmap_id} not found")
            raise HTTPException(status_code=404, detail="Resource not found")
        logger.info(f"Removed roadmap {roadmap_id}")


async def retrieve_node(node_id: UUID) -> NodeResponse:
    """Retrieve a node from the roadmap

    Args:
        node_id (UUID): Node ID

    Returns:
        NodeResponse (NodeResponse): Retrieved node
    """
    async with db.transaction() as conn:
        row = await conn.fetchrow(
            """
            SELECT *
            FROM roadmap_node
            WHERE node_id = $1
        """,
            node_id,
        )
        if not row:
            logger.error(f"Node {node_id} not found")
            raise HTTPException(status_code=404, detail="Node not found")

        logger.info(f"Retrieved node {node_id}")

    return NodeResponse(**row)


async def create_node(node: NodeCreate) -> NodeResponse:
    """Create a new node in the roadmap

    Args:
        node (NodeCreate): New node data

    Returns:
        NodeResponse (NodeResponse): Created node
    """

    logger.info(f"Creating new node for the roadmap{node.roadmap_id}")
    async with db.transaction() as conn:
        row = await conn.fetchrow(
            """
            INSERT INTO roadmap_node
            (roadmap_id, title, summary, resource_id, progress)
            VALUES ($1, $2, $3, $4, $5)
            RETURNING *
        """,
            node.roadmap_id,
            node.title,
            node.summary,
            node.resource_id,
            node.progress,
        )

        if not row:
            logger.error("Failed to create a row")
            raise HTTPException(status_code=500,
                                detail="Failed to create a row")

    return NodeResponse(**row)


async def update_node(node: NodeUpdate) -> NodeResponse:
    """Update a node in the roadmap

    Args:
        node (NodeUpdate): Updated node data
    """
    async with db.transaction() as conn:
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

        values.append(node.node_id)

        if not updates:
            logger.error("No fields provided for update")
            raise HTTPException(
                status_code=400, detail="No fields provided for update"
            )

        query = f"""
            UPDATE roadmap_node
            SET {', '.join(updates)}
            WHERE node_id = ${len(values)}
            RETURNING *
        """

        row = await conn.fetchrow(query, *values)

        if not row:
            logger.error(f"Node {node.node_id} not found")
            raise HTTPException(status_code=404, detail="Node not found")

        logger.info(f"Updated node {node.node_id}")
    return NodeResponse(**row)


async def delete_node(node_id: UUID):
    """Delete a node from the roadmap

    Args:
        node_id (UUID): Node ID

    """
    async with db.transaction() as conn:
        row = await conn.execute(
            """
            DELETE FROM roadmap_node
            WHERE node_id = $1
        """,
            node_id,
        )

        if row == "DELETE 0":
            logger.error(f"Node {node_id} not found")
            raise HTTPException(status_code=404, detail="Resource not found")

        logger.info(f"Deleted node {node_id}")


async def retrieve_link(link_id: UUID) -> LinkResponse:
    """Retrieve a link from the roadmap

    Args:
        link_id (UUID): Link ID

    Returns:
        LinkResponse (LinkResponse): Retrieved link
    """
    async with db.transaction() as conn:
        row = await conn.fetchrow(
            """
            SELECT *
            FROM roadmap_link
            WHERE link_id = $1
        """,
            link_id,
        )

        if not row:
            logger.error(f"Link {link_id} not found")
            raise HTTPException(status_code=404, detail="Link not found")

        logger.info(f"Retrieved link {link_id}")

    return LinkResponse(**row)


async def create_link(link: LinkCreate) -> LinkResponse:
    """Create a new link in the roadmap

    Args:
        link (LinkCreate): New link data

    Returns:
        LinkResponse (LinkResponse): Created link
    """

    logger.info(f"Creating new link for the roadmap {link.roadmap_id}")

    async with db.transaction() as conn:
        row = await conn.fetchrow(
            """
            INSERT INTO roadmap_link (roadmap_id, from_node, to_node)
            VALUES ($1, $2, $3)
            RETURNING *
        """,
            link.roadmap_id,
            link.from_node,
            link.to_node,
        )

        if not row:
            logger.error("Failed to create a link")
            raise HTTPException(status_code=500,
                                detail="Failed to create a link")

    return LinkResponse(**row)


async def delete_link(link_id: UUID):
    """Delete a link from the roadmap

    Args:
        link_id (UUID): Link ID

    """
    async with db.transaction() as conn:
        result = await conn.execute(
            """
            DELETE FROM roadmap_link
            WHERE link_id = $1
        """,
            link_id,
        )
        logger.info(f"Deleted link {link_id}")

        if result == "DELETE 0":
            logger.error(f"Link {link_id} not found")
            raise HTTPException(status_code=404, detail="Resource not found")


async def get_roadmap_progress(roadmap_id: UUID) -> int:
    """Get roadmap progress based on progress of each node

    Args:
        feature-profile-api (UUID): Roadmap ID

    Returns:
        Progress (int): Roadmap progress in percents

    """
    progress = db.fetch(
        """
            SELECT
                SUM(progress) / COUNT(*)
            FROM
                roadmap_node
            WHERE
                roadmap_id = $1
        """,
        roadmap_id
    )

    return int(progress)
