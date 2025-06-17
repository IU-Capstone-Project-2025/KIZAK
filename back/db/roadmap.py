from db_connector import get_conn
from models.roadmap import RoadmapNode, RoadmapLink, Roadmap, CreateNode
from typing import Awaitable
from uuid import UUID

async def get_roadmap(roadmap_id: UUID) -> Awaitable[Roadmap]:
    async with await get_conn() as conn:
        rows = await conn.fetch("""
            SELECT node_id, link_id
            FROM User_Roadmap
            WHERE roadmap_id = $1
        """, roadmap_id)

        if not rows:
            return None

        nodes = [RoadmapNode(node_id=row['node_id']) for row in rows if row['node_id'] is not None]
        links = [RoadmapLink(link_id=row['link_id']) for row in rows if row['link_id'] is not None]

        return Roadmap(nodes=nodes, links=links)

async def get_node(node_id: UUID) -> Awaitable[RoadmapNode]:
    async with await get_conn() as conn:
        row = await conn.fetchone("""
            SELECT *
            FROM Roadmap_Node
            WHERE node_id = $1
        """, node_id)

        if not row:
            return None
        
        return RoadmapNode(**dict(row))

async def create_node(new_node: CreateNode) -> RoadmapNode:
    async with await get_conn() as conn:
        record = await conn.fetchrow("""
            INSERT INTO Roadmap_Node 
            (roadmap_id, title, description, resource_type, resource_id, progress)
            VALUES ($1, $2, $3, $4, $5, $6)
            RETURNING *
        """, new_node.roadmap_id, new_node.title, new_node.description,
        new_node.resource_type, new_node.resource_id, new_node.progress)
        
        return RoadmapNode(**record)


