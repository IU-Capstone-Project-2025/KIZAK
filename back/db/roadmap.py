from db_connector import get_conn
from models.roadmap import RoadmapNode, RoadmapLink, Roadmap
from uuid import UUID

async def get_roadmap(roadmap_id: UUID) -> Roadmap:
    """Returns a complete roadmap with nodes and links.

    Args:
        roadmap_id (UUID): The UUID of the roadmap to retrieve

    Returns:
        Roadmap (Roadmap): A populated Roadmap object containing nodes and links, or
        None if no roadmap exists with the given ID
    """
    async with await get_conn() as conn:
        node_rows = await conn.fetch("""
            SELECT node_id, roadmap_id, title, summary, resource_id, progress
            FROM roadmap_node
            WHERE roadmap_id = $1
        """, roadmap_id)

        link_rows = await conn.fetch("""
            SELECT link_id, roadmap_id, from_node, to_node
            FROM roadmap_link
            WHERE roadmap_id = $1
        """, roadmap_id)

        if not node_rows and not link_rows:
            return None

        nodes = [RoadmapNode(**node) for node in node_rows]
        links = [RoadmapLink(**link) for link in link_rows]

        return Roadmap(id=roadmap_id, nodes=nodes, links=links)

async def delete_roadmap(roadmap_id: UUID) -> None:
    """Deletes roadmap and all links and nodes
    
    Args:
        roadmap_id: The UUID of the roadmap to retrieve
    """
    async with await get_conn() as conn:
        async with conn.transaction():
            await conn.execute("""
                DELETE FROM user_roadmap
                WHERE roadmap_id = $1
            """, roadmap_id)

async def create_node(node: RoadmapNode) -> RoadmapNode:
    """Add new node to db

    Args:
        node (RoadmapNode): New node

    Returns:
        RoadmapNode: Inserted node
    """
    async with await get_conn() as conn:
        async with conn.transaction():
            row = await conn.fetchrow("""
                INSERT INTO roadmap_node (roadmap_id, title, summary, resource_id, progress)
                VALUES ($1, $2, $3, $4, $5)
                RETURNING node_id
            """, node.roadmap_id, node.title, node.summary, node.resource_id, node.progress)

            node.id = row['node_id']

            return node
        
async def update_node(node: RoadmapNode) -> RoadmapNode:
    """Updates an existing node with new data.

    Args:
        node: RoadmapNode object containing the updated data.
                 Must include a valid node_id of an existing node.

    Returns:
        RoadmapNOde (RoadmapNode): The updated RoadmapNode with all current fields from the database.
    """
    async with await get_conn() as conn:
        async with conn.transaction():
            # Update node and return all fields
            row = await conn.fetchrow("""
                UPDATE roadmap_node
                SET 
                    title = $1,
                    summary = $2,
                    resource_id = $3,
                    progress = $4,
                    roadmap_id = $5
                WHERE node_id = $6
                RETURNING node_id, roadmap_id, title, summary, resource_id, progress
            """,
            node.title,
            node.summary,
            node.resource_id,
            node.progress,
            node.roadmap_id,
            node.id)

            return node

async def delete_node(node_id: UUID) -> None:
    """Deletes a node and all its associated links from the roadmap.
    
    Args:
        node_id (UUID): UUID of the node to delete
    """
    async with await get_conn() as conn:
        async with conn.transaction():
            await conn.execute(
                """
                DELETE FROM roadmap_node 
                WHERE node_id = $1
                """,
                node_id
            )

async def create_link(link: RoadmapLink) -> RoadmapLink:
    """Add new node to db

    Args:
        link (RoadmapLink): New link

    Returns:
        RoadmapLink (RoadmapLink): Same link
    """
    async with await get_conn() as conn:
        async with conn.transaction():
            row = await conn.fetchrow("""
                INSERT INTO roadmap_link (roadmap_id, from_node, to_node)
                VALUES ($1, $2, $3)
                RETURNING link_id
            """, link.roadmap_id, link.from_node, link.to_node)

            link.id = row['link_id']

            return link

async def delete_link(link_id: UUID) -> None:
    """Deletes a link from the roadmap.
    
    Args:
        link_id (UUID): UUID of the link to delete
    """
    async with await get_conn() as conn:
        async with conn.transaction():
            await conn.execute(
                """
                DELETE FROM roadmap_link 
                WHERE link_id = $1
                """,
                link_id
            )
